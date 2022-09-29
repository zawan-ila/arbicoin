FROM python:3.8.2-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app/requirements

RUN mkdir -p /app/backend/staticfiles


WORKDIR /app/requirements
COPY ./requirements.txt /app/requirements
RUN pip install -r requirements.txt

WORKDIR /app/backend
COPY . /app/backend/
