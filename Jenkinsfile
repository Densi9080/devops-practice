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
            withCredentials([string(credentialsId: 'github-token', variable: 'GH_TOKEN')]) {
                sh '''
                    echo "$GH_TOKEN" | docker login ghcr.io -u Densi9080 --password-stdin
                    cd library/backend
                    docker build -t ghcr.io/densi9080/django-backend:latest .
                    docker push ghcr.io/densi9080/django-backend:latest

                    cd ../frontend
                    docker build -t ghcr.io/densi9080/library-frontend:latest .
                    docker push ghcr.io/densi9080/library-frontend:latest
                '''
            }
            }
        }

        stage('Test') {
            steps {
                sh '''
                    docker network create test-net || true
                    if ! docker ps -a | grep "db_test"; then
                        docker run -d --name db_test --network test-net -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=library postgres:latest
                    else
                        docker stop db_test || true
                        docker rm db_test || true
                        docker run -d --name db_test --network test-net -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=library postgres:latest
                    fi
                    for i in $(seq 1 30); do
                        docker exec db_test pg_isready -U postgres > /dev/null 2>&1 && break
                        sleep 1
                    done
                    if ! docker ps -a | grep "django-test"; then
                        docker run -d --name django-test --network test-net -e POSTGRES_HOST=db_test django-backend tail -f /dev/null
                    else
                        docker stop django-test || true
                        docker rm django-test || true
                        docker run -d --name django-test --network test-net -e POSTGRES_HOST=db_test django-backend tail -f /dev/null
                    fi
                    docker exec django-test ls -la library_app/tests.py
                    docker exec django-test cat library_app/tests.py | head -n 5
                    docker exec django-test python manage.py test library_app --noinput -v 2
                    docker stop django-test && docker rm django-test
                    docker stop db_test && docker rm db_test
                    echo Тест
                '''
            }
        }
        stage('Run / Deploy') {
            when {
                expression { env.GIT_BRANCH == 'origin/main' }
                }
            steps {
                withCredentials([string(credentialsId: 'github-token', variable: 'GH_TOKEN')]){
                keepRunning{
                    sh '''
                        echo "$GH_TOKEN" | docker login ghcr.io -u Densi9080 --password-stdin
                        docker pull ghcr.io/densi9080/django-backend:latest
                        docker pull ghcr.io/densi9080/library-frontend:latest

                        docker network create library-net || true
                        if ! docker ps -a | grep "db"; then
                           docker run -d --name db --network library-net -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=library postgres:latest
                        else
                            docker stop db || true
                            docker rm db || true
                            docker run -d --name db --network library-net -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=library postgres:latest
                        fi
                        for i in $(seq 1 30); do
                            docker exec db pg_isready -U postgres > /dev/null 2>&1 && break
                            sleep 1
                        done

                        if ! docker ps -a | grep "django-app"; then
                            docker run -d --name django-app --network library-net -p 8000:8000 ghcr.io/densi9080/django-backend
                            docker exec django-app python manage.py migrate
                            docker exec -e DJANGO_SUPERUSER_USERNAME=admin -e DJANGO_SUPERUSER_EMAIL=admin@example.com -e DJANGO_SUPERUSER_PASSWORD=admin django-app python manage.py createsuperuser --noinput
                        else
                            docker stop django-app || true
                            docker rm django-app || true
                            docker run -d --name django-app --network library-net -p 8000:8000 ghcr.io/densi9080/django-backend
                            docker exec django-app python manage.py migrate
                            docker exec -e DJANGO_SUPERUSER_USERNAME=admin -e DJANGO_SUPERUSER_EMAIL=admin@example.com -e DJANGO_SUPERUSER_PASSWORD=admin django-app python manage.py createsuperuser --noinput
                        fi
                        if ! docker ps -a | grep "library-frontend"; then
                            docker run -d --name library-frontend --network library-net -p 5173:5173 ghcr.io/densi9080/library-frontend
                        else
                            docker stop library-frontend || true
                            docker rm library-frontend || true
                            docker run -d --name library-frontend --network library-net -p 5173:5173 ghcr.io/densi9080/library-frontend
                        fi
                    '''
                }
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