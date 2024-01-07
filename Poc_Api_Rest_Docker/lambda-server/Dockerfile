FROM python:3.11.4-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /jobs

RUN apk update
RUN pip install --upgrade pip

COPY ./requirements.txt /jobs/requirements.txt

RUN pip install -r /jobs/requirements.txt

COPY ./src/ /jobs
