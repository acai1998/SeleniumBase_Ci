FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 使用阿里云的 Debian 源
RUN rm -f /etc/apt/sources.list.d/* && \
    echo "deb http://mirrors.aliyun.com/debian bookworm main contrib non-free" > /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian bookworm-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian-security bookworm-security main contrib non-free" >> /etc/apt/sources.list && \
    apt-get clean && apt-get update -y

# 安装系统依赖
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    wget unzip curl gnupg xvfb fonts-liberation libnss3 libgconf-2-4 \
    libxi6 libgl1-mesa-glx libglib2.0-0 libgtk-3-0 libx11-xcb1 \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# 安装最新版 Chrome 浏览器（官方源）
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*


# 安装对应版本的 ChromeDriver（125.x）
ENV CHROMEDRIVER_VERSION=125.0.6422.76
RUN wget -O /tmp/chrome-linux64.zip \
    "https://registry.npmmirror.com/-/binary/chrome-for-testing/${CHROMEDRIVER_VERSION}/linux64/chrome-linux64.zip" && \
    unzip /tmp/chrome-linux64.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chrome-linux64.zip

# 安装 Python 依赖（清华源）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    --index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    --extra-index-url https://pypi.org/simple && \
    pip install --no-cache-dir seleniumbase pytest-html allure-pytest pytest-xdist \
    --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 复制代码
COPY . .

ENTRYPOINT ["pytest"]
