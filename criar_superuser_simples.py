#!/usr/bin/env python
"""Script para criar superuser"""
import sys
import os

# Adiciona o diretório do projeto ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'olhar_literario_django'))

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olhar_literario_django.settings')

import django
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Remove admin se existir
User.objects.filter(username='admin').delete()

# Cria novo superuser
user = User.objects.create_superuser(
    username='admin',
    email='admin@olharliterario.com',
    password='Admin@123'
)

print("=" * 60)
print("✅ SUPERUSER CRIADO COM SUCESSO!")
print("=" * 60)
print(f"Username: admin")
print(f"Email: admin@olharliterario.com")
print(f"Senha: Admin@123")
print("=" * 60)
print(f"Acesse: http://localhost:8000/admin")
print("=" * 60)
