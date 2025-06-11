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

# 安装所需工具
RUN apt-get update && apt-get install -y wget unzip gnupg ca-certificates fonts-liberation libnss3 libgconf-2-4 libxi6 libgl1-mesa-glx libglib2.0-0 libgtk-3-0 libx11-xcb1 && \
    rm -rf /var/lib/apt/lists/*

# 指定版本（Chrome 与 Chromedriver 保持一致）
ENV CHROME_VERSION=125.0.6422.141

# 下载 Chrome 和 Chromedriver
RUN wget -O /tmp/chrome-linux64.zip "https://registry.npmmirror.com/-/binary/chrome-for-testing/${CHROME_VERSION}/linux64/chrome-linux64.zip" && \
    wget -O /tmp/chromedriver-linux64.zip "https://registry.npmmirror.com/-/binary/chrome-for-testing/${CHROME_VERSION}/linux64/chromedriver-linux64.zip" && \
    unzip /tmp/chrome-linux64.zip -d /opt/ && \
    unzip /tmp/chromedriver-linux64.zip -d /opt/ && \
    ln -s /opt/chrome-linux64/chrome /usr/bin/google-chrome && \
    ln -s /opt/chromedriver-linux64/chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/google-chrome /usr/bin/chromedriver && \
    rm /tmp/*.zip


# 安装 Python 依赖（清华源）
RUN pip install --no-cache-dir -r requirements.txt \
    --index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    --extra-index-url https://mirrors.aliyun.com/pypi/simple \
    --extra-index-url https://pypi.org/simple && \
    pip install --no-cache-dir seleniumbase pytest-html allure-pytest pytest-xdist \
    --index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    --extra-index-url https://mirrors.aliyun.com/pypi/simple \
    --extra-index-url https://pypi.org/simple

# 复制代码
COPY . .

ENTRYPOINT ["pytest"]
