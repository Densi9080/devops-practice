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
                        docker network create library-net || true
                        if ! docker ps -a | grep "django-app"; then
                            docker run -d --name django-app -p 8000:8000 django-backend
                        else
                            docker stop django-app || true
                            docker rm django-app || true
                            docker run -d --name django-app -p 8000:8000 django-backend
                        fi
                        if ! docker ps -a | grep "library-frontend"; then
                            docker run -d --name library-frontend --network library-net -p 5173:5173 library-frontend
                        else
                            docker stop library-frontend || true
                            docker rm library-frontend || true
                            docker run -d --name library-frontend --network library-net -p 5173:5173 library-frontend
                        fi
                        if ! docker ps -a | grep "db"; then
                           docker run -d --name db --network library-net -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=library postgres:latest
                        else
                            docker stop db || true
                            docker rm db || true
                            docker run -d --name db -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=library postgres:latest
                        fi
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