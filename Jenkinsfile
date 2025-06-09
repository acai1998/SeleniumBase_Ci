pipeline {
    agent any
    environment {
        REPORT_DIR = 'reports'
        ALLURE_DIR = 'allure-results'
        TEST_CASE_DIR = 'test_case'
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://gitee.com/Ac1998/SeleniumBase-CI.git'
            }
        }
        stage('Setup') {
            steps {
                sh 'python -m pip install --upgrade pip'
                sh 'pip install allure-pytest seleniumbase pytest-html'
                sh 'pwd && ls'
                sh 'rm -rf 项目根目录 项目根目录@tmp'
                sh 'ls -al test_case/'
            }
        }
        stage('Test') {
            steps {
                // 不再切换目录，统一以 Jenkins 根路径为标准
                sh """
                python -m pytest ${TEST_CASE_DIR} \
                  --browser=chrome \
                  --dashboard --rs \
                  --headless \
                  --alluredir=${ALLURE_DIR} \
                  --junitxml=${REPORT_DIR}/junit.xml \
                  --html=${REPORT_DIR}/report.html
                """
            }
        }
    }
    post {
        always {
            allure includeProperties: false,
                   jdk: '',
                   results: [[path: "${ALLURE_DIR}"]]
            archiveArtifacts artifacts: "${REPORT_DIR}/*.html,${ALLURE_DIR}/**"
        }
    }
}
