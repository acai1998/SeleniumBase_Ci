FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 替换为阿里云的 Debian 镜像源
RUN echo "deb http://mirrors.aliyun.com/debian/ stable main non-free contrib" > /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian-security stable-security main contrib" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian/ stable-updates main contrib" >> /etc/apt/sources.list && \
    apt-get clean && \
    apt-get update

# 安装系统依赖（包含 Chrome 和 xvfb）
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg xvfb libnss3 libgconf-2-4 libxi6 libgl1-mesa-glx libglib2.0-0 libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# 使用阿里云镜像安装 Chrome 浏览器
RUN apt-get update && apt-get install -y wget gnupg && \
    wget -qO- https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] https://mirrors.aliyun.com/google-chrome/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# 设置 ChromeDriver 版本并安装
ENV CHROMEDRIVER_VERSION 109.0.5414.74
RUN wget -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver_linux64.zip

# 安装 Python 包
COPY requirements.txt .
RUN pip install -r requirements.txt --index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install seleniumbase pytest-html allure-pytest pytest-xdist --index-url https://pypi.tuna.tsinghua.edu.cn/simple
    
WORKDIR /app
COPY . .

ENTRYPOINT ["pytest"]
