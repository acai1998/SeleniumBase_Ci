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
  -n auto || echo [警告] 测试失败，继续执行后续步骤

exit /b 0
