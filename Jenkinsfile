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
                    sh 'rm -rf allure-results/* allure-report/*'

                    sh 'docker compose up -d postgres'
                    sh 'echo "Waiting for postgres to be ready..."'
                    sh '''
                        until docker compose exec -T postgres pg_isready -U postgres >/dev/null 2>&1; do
                            sleep 2
                        done
                    '''

                    def containerName = "app_test_${BUILD_NUMBER}"
                    try {
                        sh "docker compose run --name ${containerName} app pytest --alluredir=/app/allure-results -v"
                    } finally {
                        sh "docker cp ${containerName}:/app/allure-results/. ./allure-results/ || true"
                        sh "docker rm -f ${containerName} || true"
                    }
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