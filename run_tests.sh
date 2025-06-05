#!/bin/bash -xe

cd /var/jenkins_home/workspace/SeleniumBase-CI

# 清理旧环境
rm -rf venv reports latest_logs

# 创建虚拟环境
python3 -m venv venv

# 安装依赖（使用虚拟环境中的 pip）
./venv/bin/pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 运行 SeleniumBase 测试（使用虚拟环境中的 python）
./venv/bin/python -m seleniumbase run test_case/ \
  --browser=chrome \
  --headless \
  --junit-xml=reports/junit.xml \
  --report
