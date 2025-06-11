FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 使用阿里云的 Debian 源（针对 slim 镜像的修复）
RUN echo "deb http://mirrors.aliyun.com/debian/ stable main non-free contrib" > /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian-security stable-security main contrib" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian/ stable-updates main contrib" >> /etc/apt/sources.list && \
    apt-get clean && apt-get update -y

# 安装系统依赖（合并 apt 操作减少层数）
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    wget unzip curl gnupg xvfb \
    libnss3 libgconf-2-4 libxi6 libgl1-mesa-glx libglib2.0-0 libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# 使用国内镜像安装 Chrome 浏览器
RUN wget -qO- https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] https://mirrors.aliyun.com/google-chrome/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# 使用淘宝镜像安装 ChromeDriver (速度更快)
ENV CHROMEDRIVER_VERSION 109.0.5414.74
RUN wget -O /tmp/chromedriver_linux64.zip \
    "https://registry.npmmirror.com/-/binary/chromedriver/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver_linux64.zip

# 安装 Python 包 (使用清华源)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    --index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    --extra-index-url https://pypi.org/simple && \
    pip install --no-cache-dir seleniumbase pytest-html allure-pytest pytest-xdist \
    --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 复制应用代码
COPY . .

ENTRYPOINT ["pytest"]