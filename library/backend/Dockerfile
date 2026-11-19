from python:3.12-slim
copy . /django-app
workdir /django-app
run pip install -r requirements.txt
expose 8000
cmd ["python", "manage.py", "runserver", "0.0.0.0:8000"]