FROM python:3.11.7-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . . 

EXPOSE 8000

CMD python EtsiiMarktProject/manage.py makemigrations && python EtsiiMarktProject/manage.py migrate && python EtsiiMarktProject/manage.py runserver 0.0.0.0:8000