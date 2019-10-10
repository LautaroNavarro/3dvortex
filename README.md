# 3dvortext
3d vortex is a web service that allow you to print your own 3d models without a 3d printer

## CI
Travis
[![Build Status](https://travis-ci.com/LautaroNavarro/3dvortex.svg?branch=master)](https://travis-ci.com/LautaroNavarro/3dvortex)

Coverage
[![Coverage Status](https://coveralls.io/repos/github/LautaroNavarro/3dvortext/badge.svg?branch=)](https://coveralls.io/github/LautaroNavarro/3dvortext?branch=)

# Getting started

## Enviroment variables

To work fully the project will need you to define some environment variables

- AMAZON_ACCESS_KEY_ID: Amazon access key id
- AMAZON_ACCESS_SECRET_KEY: Amazon access secret key
- IMAGES_BUCKET_NAME: Bucket name in where the images are going to be uploaded
- MODELS_BUCKET_NAME: Bucket name in where the models are going to be uploaded


## Running the project

> **Note:** You will need to install docker and docker-compose before following the steps below
[docker installation](https://docs.docker.com/v17.09/engine/installation/)
[docker-compose installation](https://docs.docker.com/compose/install/)

Go the project folder and inside of it run the command below to **build** the project images

    docker-compose build

> **Note:** You will need internet access and also it could take some minutes

Run the command below to **run** the containers

    docker-compose run

> **Note:** You can access the API on localhost:8000

Run the command below to run the testsuite

    docker-compose run django pytest
