# =============================================================================
# SeleniumBase CI 测试执行镜像
# =============================================================================
# 策略：
#   - 环境（Python / Chrome / ChromeDriver / pytest）锁定在镜像内
#   - 测试代码不打包进镜像，由 entrypoint.sh 在运行时从 Git 仓库 clone
#   - 每次 Chrome 大版本更新时重新 build 并 push 新镜像
# =============================================================================

FROM python:3.11-slim

# ── 基础环境变量 ──────────────────────────────────────────────────────────────
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # SeleniumBase 无头模式（容器内无显示器）
    SB_HEADLESS=true \
    # ChromeDriver 固定路径，避免 SeleniumBase 运行时重新下载
    CHROMEDRIVER_PATH=/usr/local/bin/chromedriver \
    # Chrome 与 ChromeDriver 版本（两者必须严格匹配，升级时同步修改）
    CHROME_VERSION=131.0.6778.85

# ── 1. 替换为阿里云 Debian 镜像源，安装系统依赖 ──────────────────────────────
RUN rm -f /etc/apt/sources.list.d/* && \
    echo "deb http://mirrors.aliyun.com/debian bookworm main contrib non-free" > /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian bookworm-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian-security bookworm-security main contrib non-free" >> /etc/apt/sources.list && \
    apt-get clean && apt-get update -y && \
    apt-get install -y --no-install-recommends \
        # 下载 / 解压工具
        wget curl unzip ca-certificates gnupg \
        # 版本控制（entrypoint 里 git clone 测试代码用）
        git \
        # Chrome 运行时系统库
        libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 \
        libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 \
        libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 \
        libxss1 libxtst6 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
        libdrm2 libgbm1 libasound2 \
        # 中文字体（截图含中文时不乱码）
        fonts-liberation fonts-wqy-zenhei \
    && rm -rf /var/lib/apt/lists/*

# ── 2. 安装 Chrome for Testing（与 ChromeDriver 版本严格匹配）────────────────
# 优先 npmmirror 国内源，失败回退 Google 官方 storage
RUN set -e; \
    TMP_ZIP=/tmp/chrome-linux64.zip; \
    curl -fL --connect-timeout 30 --max-time 180 \
        "https://registry.npmmirror.com/-/binary/chrome-for-testing/${CHROME_VERSION}/linux64/chrome-linux64.zip" \
        -o "$TMP_ZIP" 2>/dev/null \
    || curl -fL --connect-timeout 30 --max-time 300 \
        "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chrome-linux64.zip" \
        -o "$TMP_ZIP"; \
    unzip -q "$TMP_ZIP" -d /opt/; \
    ln -sf /opt/chrome-linux64/chrome /usr/bin/google-chrome; \
    chmod +x /opt/chrome-linux64/chrome; \
    rm -f "$TMP_ZIP"; \
    google-chrome --version

# ── 3. 安装 ChromeDriver（与 Chrome 版本严格对齐）────────────────────────────
RUN set -e; \
    TMP_ZIP=/tmp/chromedriver-linux64.zip; \
    curl -fL --connect-timeout 30 --max-time 180 \
        "https://registry.npmmirror.com/-/binary/chrome-for-testing/${CHROME_VERSION}/linux64/chromedriver-linux64.zip" \
        -o "$TMP_ZIP" 2>/dev/null \
    || curl -fL --connect-timeout 30 --max-time 300 \
        "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip" \
        -o "$TMP_ZIP"; \
    unzip -q "$TMP_ZIP" -d /tmp/chromedriver_extract; \
    mv /tmp/chromedriver_extract/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver; \
    chmod +x /usr/local/bin/chromedriver; \
    rm -rf "$TMP_ZIP" /tmp/chromedriver_extract; \
    chromedriver --version

# ── 4. 安装 Python 测试依赖（不含测试代码，测试代码运行时 clone）──────────────
COPY requirements-runner.txt /tmp/requirements-runner.txt
RUN pip install --no-cache-dir \
    -i https://mirrors.aliyun.com/pypi/simple/ \
    --trusted-host mirrors.aliyun.com \
    -r /tmp/requirements-runner.txt && \
    rm -f /tmp/requirements-runner.txt

# ── 5. 把 ChromeDriver 同步到 SeleniumBase 驱动目录，防止运行时走外网下载 ──────
RUN python - <<'PY'
import os, shutil, seleniumbase
sb_dir = os.path.join(os.path.dirname(seleniumbase.__file__), 'drivers')
os.makedirs(sb_dir, exist_ok=True)
src = '/usr/local/bin/chromedriver'
dst = os.path.join(sb_dir, 'chromedriver')
shutil.copy2(src, dst)
os.chmod(dst, 0o755)
print(f'chromedriver synced to SeleniumBase drivers dir: {dst}')
PY

# ── 6. 复制入口脚本 ────────────────────────────────────────────────────────────
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# ── 7. 工作目录（entrypoint 会在这里 clone 代码）─────────────────────────────
WORKDIR /workspace

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
