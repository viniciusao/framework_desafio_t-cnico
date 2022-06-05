FROM python:3.8
WORKDIR /opt/framework_test
COPY . /opt/framework_test
RUN pip install -r requirements.txt
RUN coverage run -m pytest desafio_framework/tests/tests.py
RUN coverage report
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]