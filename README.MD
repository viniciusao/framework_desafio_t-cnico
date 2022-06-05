# Usage

### No docker.
1. pip install -r requirements.txt
2. coverage run -m pytest desafio_framework/tests/tests.py
3. coverage report
4. python manage.py runserver
5. test_framework.postman_collection.json

### Docker.
1. sudo docker build -t test_framework .
2. sudo docker container run --name testando -it -p 8000:8000 test_framework
3. test_framework.postman_collection.json