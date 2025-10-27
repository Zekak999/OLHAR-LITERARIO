#!/bin/bash
set -e

echo "📦 Instalando dependências..."
pip install -r requirements.txt

echo "📁 Entrando no diretório do projeto Django..."
cd olhar_literario_django

echo " Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "✅ Build concluído!"
