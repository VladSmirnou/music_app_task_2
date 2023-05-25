FROM python:3.11-bullseye

WORKDIR /flask_music/app 

COPY . /flask_music/app

EXPOSE 5000

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
