@echo off
setlocal
echo [Windows] Upgrading pip...
python -m pip install --upgrade pip

echo [Windows] Installing dependencies from requirements.txt...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

echo [Windows] Installing additional pytest plugins...
pip install pytest pytest-html allure-pytest pytest-xdist

echo [Windows] Running tests...
python -m pytest test_case ^
  --browser=chrome ^
  --dashboard --rs ^
  --headless ^
  --alluredir=allure-results ^
  --junitxml=reports\junit.xml ^
  --html=reports\report.html ^
  -n auto

endlocal
