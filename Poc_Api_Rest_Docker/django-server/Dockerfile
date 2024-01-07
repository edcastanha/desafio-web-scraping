FROM python:3.11.4-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk update \
    && apk add --no-cache mariadb-connector-c-dev \
                          build-base \
                          mariadb-dev \
                          postgresql-dev \
                          libffi-dev \
                          zlib-dev \
                          jpeg-dev \
                          && pip install --upgrade pip

COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app
