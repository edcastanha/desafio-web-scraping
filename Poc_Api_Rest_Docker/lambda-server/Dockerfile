FROM python:3.11.4-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /jobs

RUN apk update \
    && apk add --no-cache mariadb-connector-c-dev \
                          build-base \
                          mariadb-dev \
                          postgresql-dev \
                          libffi-dev \
                          zlib-dev \
                          jpeg-dev \
                          && pip install --upgrade pip


COPY ./requirements.txt /jobs/requirements.txt

RUN pip install -r /jobs/requirements.txt

COPY ./src/ /jobs
