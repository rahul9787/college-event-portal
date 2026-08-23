pipeline {

    agent any

    environment {
        AWS_REGION = 'us-east-1'
        AWS_ACCOUNT_ID = '817137372823'

        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

        FRONTEND_IMAGE = "${ECR_REGISTRY}/college-event-portal-frontend:latest"
        BACKEND_IMAGE  = "${ECR_REGISTRY}/college-event-portal-backend:latest"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/rahul9787/college-event-portal.git'
            }
        }

        stage('Check Docker') {
            steps {
                sh 'docker --version'
                sh 'docker compose version'
                sh 'aws --version'
            }
        }

        stage('Build') {
            steps {
                sh '''
                    docker build -t college-event-portal-frontend:latest ./frontend
                    docker build -t college-event-portal-backend:latest ./backend
                '''
            }
        }

        stage('ECR Login') {
            steps {
                sh '''
                    aws ecr get-login-password --region $AWS_REGION |
                    docker login --username AWS --password-stdin $ECR_REGISTRY
                '''
            }
        }

        stage('Tag Images') {
            steps {
                sh '''
                    docker tag college-event-portal-frontend:latest $FRONTEND_IMAGE
                    docker tag college-event-portal-backend:latest $BACKEND_IMAGE
                '''
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                    docker push $FRONTEND_IMAGE
                    docker push $BACKEND_IMAGE
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker compose down
                    docker compose pull
                    docker compose up -d
                '''
            }
        }

        stage('Verify') {
            steps {
                sh '''
                    docker ps
                    docker compose ps
                '''
            }
        }
    }
}
