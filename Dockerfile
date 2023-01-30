# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /python-docker

RUN apt-get update && apt-get -y install libpq-dev gcc 

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt



COPY . .

EXPOSE 5000
ENV FLASK_APP=manage.py

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
