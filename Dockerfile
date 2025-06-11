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

# 安装最新 Chrome 浏览器（从清华源下载 .deb 包）
RUN wget -O /tmp/google-chrome.deb https://mirrors.tuna.tsinghua.edu.cn/google/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_125.0.6422.141-1_amd64.deb && \
    apt-get update -y && \
    apt-get install -y /tmp/google-chrome.deb && \
    rm /tmp/google-chrome.deb

# 安装对应版本的 ChromeDriver（125.x）
ENV CHROMEDRIVER_VERSION 125.0.6422.76
RUN wget -O /tmp/chromedriver_linux64.zip \
    "https://registry.npmmirror.com/-/binary/chromedriver/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver_linux64.zip

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
