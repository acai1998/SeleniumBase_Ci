#!/bin/bash -xe

cd /var/jenkins_home/workspace/SeleniumBase-CI

# 安装依赖
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 执行 SeleniumBase 测试（注意：直接使用 seleniumbase CLI）
python test_case/ \
  --browser=chrome \
  --headless \
  --junit-xml=reports/junit.xml \
  --report
