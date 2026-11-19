pipeline {
    agent any
    
    environment {
        VENV_DIR = 'venv'
        APP_PORT = '8000'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh '''
                    cd library/backend
                    docker build -t django-backend .
                    cd ..
                    cd frontend
                    docker build -t library-frontend .
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    if ! docker ps -a | grep "django-test"; then
                        docker run -d --name django-test django-backend tail -f /dev/null
                    else
                        docker stop django-test || true
                        docker rm django-test || true
                        docker run -d --name django-test django-backend tail -f /dev/null
                    fi
                    # docker exec django-test python manage.py test
                    docker stop django-test && docker rm django-test
                    echo Тест
                '''
            }
        }
        stage('Send'){
            steps {
                sh '''
                    echo Маша попа
                '''

            }
        }
        stage('Run / Deploy') {
            when {
                expression { env.GIT_BRANCH == 'origin/main' }
                }
            steps {
                keepRunning{
                    sh '''
                        docker stop django-app || true
                        docker rm django-app || true
                        docker run -d --name django-app -p 8000:8000 django-backend
                        docker run -d --name library-frontend -p 5173:5173 library-frontend
                        docker run -d --name db -p 5432:5432 postgres:latest
                    '''
                }
            }
        }
    }

    post {
        failure {
            sh 'cat django.log || true'
        }
    }
}