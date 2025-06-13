#!/bin/bash
set -e  # 一旦有命令出错就停止脚本

echo "🔧 升级 pip..."
python -m pip install --upgrade pip

echo "📦 安装依赖（requirements.txt）..."
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

echo "🧪 安装 pytest 扩展插件..."
python -m pip install pytest pytest-html allure-pytest pytest-xdist

echo "🚀 开始执行测试..."
python -m pytest test_case/ \
  --browser=chrome \
  --dashboard --rs \
  --headless \
  --alluredir=allure-results \
  --junitxml=reports/junit.xml \
  --html=reports/report.html
  -n auto