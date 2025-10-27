"""
Script para criar UserProfile para todos os usuários que não têm
Execute este script após fazer deploy para garantir que não haverá erros
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olhar_literario_django.settings')
django.setup()

from django.contrib.auth.models import User
from books.models import UserProfile

def criar_profiles_faltantes():
    """
    Cria UserProfile para todos os usuários que não têm
    """
    print("\n" + "=" * 70)
    print("🔧 CRIANDO USERPROFILE PARA USUÁRIOS SEM PERFIL")
    print("=" * 70)
    
    usuarios = User.objects.all()
    criados = 0
    ja_existentes = 0
    
    for usuario in usuarios:
        profile, created = UserProfile.objects.get_or_create(user=usuario)
        if created:
            criados += 1
            print(f"✅ Profile criado para: {usuario.username}")
        else:
            ja_existentes += 1
            print(f"ℹ️  Profile já existe para: {usuario.username}")
    
    print("=" * 70)
    print(f"📊 RESUMO:")
    print(f"   • Total de usuários: {usuarios.count()}")
    print(f"   • Profiles criados: {criados}")
    print(f"   • Profiles já existentes: {ja_existentes}")
    print("=" * 70 + "\n")

if __name__ == '__main__':
    criar_profiles_faltantes()
