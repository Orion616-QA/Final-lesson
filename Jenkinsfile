pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {
        // перевірка коду з репозиторію
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        // будуємо контейнери
        stage('Build containers') {
            steps {
                script {
                    sh 'mkdir -p allure-results allure-reports && chmod 777 allure-results allure-reports'
                    sh 'docker compose build'
                }
            }
        }
        // запускаємо тести в контейнерах
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

        // відправляємо лист якщо успішно
        success {
            emailext body: "Job '${env.JOB_NAME} #${env.BUILD_NUMBER}' succeeded.\n${env.BUILD_URL}",
                     subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                     to: "developer@ithillel.ua"
        }

        // відправляємо лист якщо помилка
        failure {
            emailext body: "Job '${env.JOB_NAME} #${env.BUILD_NUMBER}' failed.\n${env.BUILD_URL}",
                     subject: "FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                     to: "developer@ithillel.ua"
        }
    }
}