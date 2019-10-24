FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN apt-get update
RUN apt-get install blender -y
RUN pip3 install -r requirements.txt
COPY ./src /app
