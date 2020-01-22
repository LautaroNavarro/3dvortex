FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
RUN apt-get update
COPY requirements.txt /app/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY ./src /app
RUN mkdir /tmp/models
