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
                    sh 'docker compose build'
                }
            }
        }

        stage('Run tests in containers') {
            steps {
                script {
                    // Запуск тестов, завершение по коду контейнера app
                    sh 'docker compose up --abort-on-container-exit --exit-code-from app'
                }
            }
        }
    }

    post {
        always {
            // Публикация Allure после тестов
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]

            // Остановка и очистка окружения
            sh 'docker compose down -v'
        }

        success {
            emailext body: "Job '${env.JOB_NAME} #${env.BUILD_NUMBER}' succeeded.\n${env.BUILD_URL}",
                     subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                     to: "InsertYour@Mail.Here"
        }

        failure {
            emailext body: "Job '${env.JOB_NAME} #${env.BUILD_NUMBER}' failed.\n${env.BUILD_URL}",
                     subject: "FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                     to: "InsertYour@Mail.Here"
        }
    }
}