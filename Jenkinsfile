
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
        AWS_ACCOUNT_ID = '620503470929'
        ECR_REGISTRY = '620503470929.dkr.ecr.ap-south-1.amazonaws.com'
        ECR_REPOSITORY = '8byte-devops-app'
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

        stage('Verify AWS Credentials') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'aws-deploy-credentials',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh '''
                        set +x
                        export AWS_DEFAULT_REGION=${AWS_REGION}

                        aws sts get-caller-identity \
                          --query Arn --output text

                        aws sts get-caller-identity \
                          --query Arn --output text \
                          | grep 'jenkins-deploy-user'
                    '''
                }
            }
        }

        stage('Login to AWS ECR') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'aws-deploy-credentials',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh '''
                        set +x
                        export AWS_DEFAULT_REGION=${AWS_REGION}

                        aws ecr get-login-password \
                          --region ${AWS_REGION} \
                        | docker login \
                          --username AWS \
                          --password-stdin ${ECR_REGISTRY}
                    '''
                }
            }
        }

        stage('Push Image to ECR') {
            steps {
                sh '''
                    docker tag \
                      ${IMAGE_NAME}:${BUILD_NUMBER} \
                      ${ECR_REGISTRY}/${ECR_REPOSITORY}:${BUILD_NUMBER}

                    docker push \
                      ${ECR_REGISTRY}/${ECR_REPOSITORY}:${BUILD_NUMBER}
                '''
            }
        }
    }

    post {
        success {
            echo 'CI pipeline and ECR image publishing completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Check the failed stage in Console Output.'
        }
        always {
            sh 'docker logout ${ECR_REGISTRY} || true'
        }
    }
}
