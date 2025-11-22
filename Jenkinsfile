pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build containers') {
            steps {
                script {
                    sh 'mkdir -p allure-results allure-reports && chmod 777 allure-results allure-reports'
                    sh 'docker compose build'
                }
            }
        }

        stage('Run tests in containers') {
            steps {
                script {
                    sh 'docker compose down -v --remove-orphans || true'
                    sh 'docker compose up --abort-on-container-exit --exit-code-from app'
                }
            }
        }
    }

    post {
        always {
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]

            sh 'docker compose down -v'
        }

        success {
            emailext body: "Job '${env.JOB_NAME} #${env.BUILD_NUMBER}' succeeded.\n${env.BUILD_URL}",
                     subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                     to: "ab100190pin@gmail.com"
        }

        failure {
            emailext body: "Job '${env.JOB_NAME} #${env.BUILD_NUMBER}' failed.\n${env.BUILD_URL}",
                     subject: "FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                     to: "ab100190pin@gmail.com"
        }
    }
}