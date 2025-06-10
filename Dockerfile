# 使用官方 Python 镜像
FROM python:3.10-slim

# 安装 Chrome 和相关依赖
RUN apt-get update && \
    apt-get install -y wget gnupg unzip xvfb libxi6 libgconf-2-4 default-jdk && \
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# 安装 ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+') && \
    DRIVER_VERSION=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}) && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${DRIVER_VERSION}/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin && \
    chmod +x /usr/local/bin/chromedriver

# 设置工作目录
WORKDIR /app

# 拷贝文件
COPY . /app

# 安装 Python 依赖
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install allure-pytest seleniumbase pytest-html

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 入口命令
CMD ["bash", "run_tests.sh"]
