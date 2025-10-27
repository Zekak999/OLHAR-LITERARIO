#!/usr/bin/env python
"""
Script para limpar referências de fotos de perfil que não existem no disco
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olhar_literario_django.settings')
django.setup()

from books.models import UserProfile

def limpar_fotos_perdidas():
    """Remove referências de fotos que não existem no disco"""
    perfis_atualizados = 0
    
    for perfil in UserProfile.objects.all():
        if perfil.foto:
            # Verificar se o arquivo existe
            caminho_completo = perfil.foto.path
            if not os.path.exists(caminho_completo):
                print(f"❌ Foto não encontrada: {perfil.foto.name}")
                print(f"   Usuário: {perfil.user.username}")
                print(f"   Caminho: {caminho_completo}")
                
                # Limpar referência
                perfil.foto = None
                perfil.save()
                perfis_atualizados += 1
                print(f"   ✅ Referência removida\n")
            else:
                print(f"✅ Foto OK: {perfil.foto.name} - Usuário: {perfil.user.username}")
    
    if perfis_atualizados > 0:
        print(f"\n🎉 {perfis_atualizados} perfil(is) atualizado(s)")
    else:
        print("\n✅ Todas as fotos estão OK!")

if __name__ == '__main__':
    print("🔍 Verificando fotos de perfil...\n")
    limpar_fotos_perdidas()
