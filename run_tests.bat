@echo off
echo [Windows] Installing dependencies...
python -m pip install --upgrade pip
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
pip install pytest pytest-html allure-pytest seleniumbase

echo [Windows] Running tests...
python -m pytest test_case/ ^
  --browser=chrome ^
  --dashboard --rs ^
  --headless ^
  --alluredir=allure-results ^
  --junitxml=reports/junit.xml ^
  --html=reports/report.html
