FROM python:3.10-slim

# 安装系统依赖（包含 Chrome 和 xvfb）
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg xvfb libnss3 libgconf-2-4 libxi6 libgl1-mesa-glx libglib2.0-0 libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# 安装 Chrome 浏览器
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# 设置 ChromeDriver 版本并安装
ENV CHROMEDRIVER_VERSION 124.0.6367.91
RUN wget -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver_linux64.zip

# 安装 Python 包
COPY requirements.txt .
RUN pip install -r requirements.txt && \
    pip install seleniumbase pytest-html allure-pytest pytest-xdist

WORKDIR /app
COPY . .

ENTRYPOINT ["pytest"]
