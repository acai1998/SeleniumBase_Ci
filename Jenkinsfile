pipeline {
    agent {
        docker {
            image 'seleniumbase-test:latest'
            args '--shm-size=2g'
        }
    }
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
        stage('Test (Parallel)') {
            steps {
                sh """
                    rm -rf ${WORKSPACE}/${ALLURE_DIR} && mkdir -p ${WORKSPACE}/${ALLURE_DIR}
                    pytest ${TEST_CASE_DIR} \
                      --browser=chrome \
                      --dashboard --rs \
                      --headless \
                      --alluredir=${ALLURE_DIR} \
                      --junitxml=${REPORT_DIR}/junit.xml \
                      --html=${REPORT_DIR}/report.html \
                      -n auto
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
