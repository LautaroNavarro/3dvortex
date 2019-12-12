FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
RUN apt-get update
RUN apt-get install blender -y
COPY requirements.txt /app/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY ./src /app
