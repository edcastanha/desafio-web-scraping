#!/usr/bin/env bash
# exit on error
set -o errexit

MARKER_FILE=/app/.initialized

if [ ! -f "$MARKER_FILE" ]; then
    
    # Aplicar migrações do banco de dados do Django para o PostgreSQL
    python manage.py makemigrations
    python manage.py migrate 
    # Coletar arquivos estáticos
    python manage.py collectstatic --no-input

    # Configurar o banco de dados MySQL
    # Exemplo para criar um banco de dados MySQL e conceder privilégios ao usuário
    # Certifique-se de ajustar de acordo com suas necessidades reais

    # Criar o banco de dados
    echo "CREATE DATABASE IF NOT EXISTS jobsDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" | mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD

    # Executar migrações para o banco de dados MySQL
    python manage.py migrate --database=mysql_db

    # Executar criacao do superuser para acesso ao Django Admin do projeto
    python setup.py

    touch "$MARKER_FILE"
else
    echo "Já inicializado. Saltar a configuração."
fi