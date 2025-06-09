pipeline {
    agent any
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
                sh 'cd /var/lib/jenkins/workspace/SeleniumBaseCI'
                sh 'pwd'
                sh 'ls'
                sh 'rm -rf 项目根目录 项目根目录@tmp'
                sh 'ls -al test_case/'
            }
        }
        stage('Test') {
            steps {
                dir('项目根目录') {
                    sh '''
                    python -m pytest /var/lib/jenkins/workspace/SeleniumBaseCI/test_case/ \
                      --browser=chrome \
                      --dashboard --rs \
                      --headless \
                      --alluredir=allure-results \
                      --junitxml=reports/junit.xml \
                      --html=reports/report.html
                    '''
                }
            }
        }
    }
    post {
        always {
            // 正确归档 allure 和 html 报告（注意路径在项目根目录内）
            allure includeProperties: false,
                   jdk: '',
                   results: [[path: '项目根目录/allure-results']]
            archiveArtifacts artifacts: '项目根目录/reports/*.html,项目根目录/allure-results/**'
        }
    }
}
