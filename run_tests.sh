#!/bin/bash

# 设置环境变量（根据实际情况调整）
export PATH=$PATH:/usr/local/bin
WORKSPACE="/var/lib/jenkins/workspace/SeleniumBase-CI"
REPORT_DIR="${WORKSPACE}/reports"

# 创建报告目录
mkdir -p "${REPORT_DIR}"

# 安装必要依赖（包含pytest）
echo "=== 安装Python依赖 ==="
python -m pip install --upgrade pip
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple \
    pytest \
    pytest-html \
    seleniumbase \
    -r requirements.txt

# 检查pytest是否安装成功
echo "=== 检查pytest版本 ==="
python -m pytest --version

# 运行测试
echo "=== 开始执行测试 ==="
python -m pytest "${WORKSPACE}/test_case/" \
    --browser=chrome \
    --headless \
    --junitxml="${REPORT_DIR}/junit.xml" \
    --html="${REPORT_DIR}/report.html"

# 检查测试结果
TEST_RESULT=$?
echo "=== 测试执行完成，退出码: ${TEST_RESULT} ==="

# 生成Allure报告（如果配置了Allure）
echo "=== 生成Allure报告 ==="
/var/lib/jenkins/tools/ru.yandex.qatools.allure.jenkins.tools.AllureCommandlineInstallation/Allure/bin/allure \
    generate "${WORKSPACE}/temp" -c -o "${REPORT_DIR}/allure-report"

exit $TEST_RESULT
