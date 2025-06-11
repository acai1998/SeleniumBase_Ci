FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 使用国内 Debian 源（阿里云）
RUN sed -i 's@http://deb.debian.org@http://mirrors.aliyun.com@g' /etc/apt/sources.list && \
    sed -i 's@http://security.debian.org@http://mirrors.aliyun.com@g' /etc/apt/sources.list && \
    apt-get clean && apt-get update

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg ca-certificates fonts-liberation \
    xvfb libnss3 libgconf-2-4 libxi6 libgl1-mesa-glx libglib2.0-0 libgtk-3-0 \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# 安装 Google Chrome（使用清华镜像中转）
RUN wget -O /tmp/google-chrome.deb https://registry.npmmirror.com/-/binary/chrome/deb/google-chrome-stable_current_amd64.deb && \
    apt install -y /tmp/google-chrome.deb && \
    rm /tmp/google-chrome.deb

# 安装 ChromeDriver（使用清华镜像）
ENV CHROMEDRIVER_VERSION 109.0.5414.74
RUN wget -O /tmp/chromedriver_linux64.zip https://registry.npmmirror.com/-/binary/chromedriver/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver_linux64.zip

# 安装 Python 依赖（使用清华 PyPI 源）
COPY requirements.txt .
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install -r requirements.txt && \
    pip install seleniumbase pytest-html allure-pytest pytest-xdist

# 拷贝项目文件
COPY . .

ENTRYPOINT ["pytest"]
