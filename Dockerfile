# pull official base image
FROM python:3.8.13-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
COPY ./requirements-test.txt /usr/src/app/requirements-test.txt
RUN pip install -r requirements.txt
RUN pip install -r requirements-test.txt

# copy project
COPY . /usr/src/app/
