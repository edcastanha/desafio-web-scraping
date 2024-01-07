FROM python:3.11-alpine3.19

# Impede o Python de escrever ficheiros pyc para o disco (equivalente à opção python -B)
ENV PYTHONDONTWRITEBYTECODE 1

# Assegura que a saída Python é enviada diretamente para o terminal sem a colocar em buffer primeiro
ENV PYTHONUNBUFFERED 1

# Expondo path
WORKDIR /api/

RUN apk update \
    && apk add --no-cache mariadb-connector-c-dev \
                          build-base \
                          mariadb-dev \
                          postgresql-dev \
                          libffi-dev \
                          zlib-dev \
                          jpeg-dev \
                          && pip install --upgrade pip

# Adiciona usuário 'api' (caso necessário)
RUN adduser -D api

# Copia os arquivos do diretório src para o diretório de trabalho
COPY . /api/

# Instalação das dependências do Python
RUN pip install -r /api/requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--workers=1", "--timeout=3600", "--bind=0.0.0.0:5000", "app:create_app()"]