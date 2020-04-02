FROM python:3.7-alpine
RUN apk add --update --no-cache g++ alpine-sdk postgresql postgresql-dev libffi libffi-dev openrc bash
WORKDIR /tochka_test
COPY . .
RUN pip install pipenv
RUN pipenv install
