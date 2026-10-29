pipeline {
    agent any

    environment {
        IMAGE_NAME  = 'iris-mlops-app'
        // Full path to Python so the pipeline works regardless of the Jenkins
        // service account PATH (LocalSystem does not inherit user PATH entries).
        PYTHON      = 'C:\\Users\\SHREEYA\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '"%PYTHON%" -m venv venv'
                bat 'venv\\Scripts\\python.exe -m pip install --upgrade pip'
                bat 'venv\\Scripts\\python.exe -m pip install -r requirements.txt'
            }
        }

        stage('Train Model') {
            steps {
                bat 'venv\\Scripts\\python.exe train.py'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'venv\\Scripts\\python.exe -m pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '"%PYTHON%" -m pip download -r requirements.txt --platform manylinux_2_17_x86_64 --platform manylinux2014_x86_64 --python-version 3.11 --only-binary=:all: -d wheels'
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
            echo 'Pipeline finished successfully. App: http://localhost:5000 | Prometheus: http://localhost:9090 | Grafana: http://localhost:3000'
        }
        failure {
            echo 'Pipeline failed. Check the console output above for details.'
        }
    }
}
