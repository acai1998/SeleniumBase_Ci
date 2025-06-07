# 安装依赖
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 运行测试，输出 HTML 和 JUnit 报告
python -m seleniumbase run test_case/ \
  --browser=chrome \
  --headless \
  --junit-xml=reports/junit.xml \
  --report
