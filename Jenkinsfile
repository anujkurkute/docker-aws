
pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        skipDefaultCheckout(true)
    }

    environment {
        IMAGE_NAME = '8byte-devops-app'
        AWS_REGION = 'ap-south-1'
        ECR_REGISTRY = '620503470929.dkr.ecr.ap-south-1.amazonaws.com'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git log -1 --oneline'
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:test \
                      -f Dockerfile.test .
                    docker run --rm ${IMAGE_NAME}:test
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                      -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Verify Image') {
            steps {
                sh '''
                    docker image inspect \
                      ${IMAGE_NAME}:${BUILD_NUMBER} \
                      --format '{{.Id}}'
                '''
            }
        }
    }

    post {
        success {
            echo 'CI pipeline completed successfully.'
        }
        failure {
            echo 'CI pipeline failed. Check console output.'
        }
    }
}
