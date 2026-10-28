pipeline {
    agent any

    environment {
        IMAGE_NAME = 'iris-mlops-app'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\python -m pip install --upgrade pip'
                bat 'venv\\Scripts\\python -m pip install -r requirements.txt'
            }
        }

        stage('Train Model') {
            steps {
                bat 'venv\\Scripts\\python train.py'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'venv\\Scripts\\python -m pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%BUILD_NUMBER% -t %IMAGE_NAME%:latest .'
            }
        }

        stage('Deploy (App + Prometheus + Grafana)') {
            steps {
                bat 'docker compose up -d --build'
            }
        }
    }

    post {
        success {
            echo 'Pipeline finished. App: http://localhost:5000 | Prometheus: http://localhost:9090 | Grafana: http://localhost:3000'
        }
        failure {
            echo 'Pipeline failed. Check the console output.'
        }
    }
}
