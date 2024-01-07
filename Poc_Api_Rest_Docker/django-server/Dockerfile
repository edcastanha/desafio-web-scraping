FROM python:3.11.4-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
EXPOSE 7000

RUN apk update
RUN pip install --upgrade pip

COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt


COPY . /app

CMD ["/bin/sh","/app/entrypoint.sh"]