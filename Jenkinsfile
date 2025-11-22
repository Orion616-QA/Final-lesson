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
                    // создаем папки один раз, не нужно chmod каждый раз
                    sh 'mkdir -p allure-results allure-report || true'
                    sh 'docker compose build'
                }
            }
        }

        stage('Run tests') {
            steps {
                script {
                    // поднимаем и запускаем контейнеры
                    sh 'docker compose up --abort-on-container-exit --exit-code-from app'
                }
            }
        }
    }

    post {
        always {
            // Генерация отчета через Jenkins Allure Plugin
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]

            // Останавливаем и удаляем контейнеры
            sh 'docker compose down -v'
        }

        success {
            emailext body: "Job '${env.JOB_NAME} #${env.BUILD_NUMBER}' succeeded.\n${env.BUILD_URL}",
                     subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                     to: "developer@ithillel.ua"
        }

        failure {
            emailext body: "Job '${env.JOB_NAME} #${env.BUILD_NUMBER}' failed.\n${env.BUILD_URL}",
                     subject: "FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                     to: "developer@ithillel.ua"
        }
    }
}