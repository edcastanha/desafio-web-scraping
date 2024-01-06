FROM python:alpine3.19

# Impede o Python de escrever ficheiros pyc para o disco (equivalente à opção python -B)
ENV PYTHONDONTWRITEBYTECODE 1

# Assegura que a saída Python é enviada diretamente para o terminal sem a colocar em buffer primeiro
ENV PYTHONUNBUFFERED 1

WORKDIR /home/api/

# Adiciona usuário 'api' (caso necessário)
RUN adduser -D api

# Copia os arquivos do diretório src para o diretório de trabalho
COPY ./src /home/api/

# Instalação das dependências do Python
RUN pip install -r /home/api/requirements.txt
