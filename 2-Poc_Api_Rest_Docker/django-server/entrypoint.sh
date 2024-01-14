#!/usr/bin/env bash
# exit on error
set -o errexit

# Aplicar migrações do banco de dados do Django para o PostgreSQL
python manage.py makemigrations
python manage.py migrate 
# Coletar arquivos estáticos
python manage.py collectstatic --no-input

# Executar criacao do superuser para acesso ao Django Admin do projeto
python setup.py
