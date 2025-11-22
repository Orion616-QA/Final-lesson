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
                    sh 'mkdir -p allure-results allure-report || true'
                    sh 'docker compose build'
                }
            }
        }

        stage('Run tests') {
            steps {
                script {
                    sh '''

                rm -rf allure-results/* allure-report/*

                docker compose up -d postgres
                docker compose ps
                echo "Waiting for postgres to be ready..."
                until docker compose exec -T postgres pg_isready -U postgres >/dev/null 2>&1; do
                    sleep 2
                done

                docker compose run --rm app pytest --alluredir=/app/allure-results -v
            '''
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
                     to: "developer@ithillel.ua"
        }

        failure {
            emailext body: "Job '${env.JOB_NAME} #${env.BUILD_NUMBER}' failed.\n${env.BUILD_URL}",
                     subject: "FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                     to: "developer@ithillel.ua"
        }
    }
}