#!/bin/bash
set -e

echo "🗄️ Aplicando migrações do banco de dados..."
cd olhar_literario_django
python manage.py migrate --noinput

echo "🚀 Iniciando servidor Gunicorn..."
exec gunicorn olhar_literario_django.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120
