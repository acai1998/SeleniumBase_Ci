@echo off
setlocal
echo [Windows] Upgrading pip...
python -m pip install --upgrade pip

echo [Windows] Installing dependencies...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
pip install pytest pytest-html allure-pytest pytest-xdist seleniumbase

echo [Windows] Running tests...
python -m pytest test_case ^
  --browser=chrome ^
  --dashboard --rs ^
  --headless ^
  --alluredir=allure-results ^
  --junitxml=reports\junit.xml ^
  --html=reports\report.html ^
:: 如果测试失败，返回非零退出码
if %errorlevel% neq 0 (
    echo [错误] 测试失败，构建将终止
    exit /b %errorlevel%
)

echo [成功] 所有测试已通过
exit /b 0
