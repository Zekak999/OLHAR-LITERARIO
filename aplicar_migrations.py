#!/usr/bin/env python
"""
Script para aplicar migrations do novo sistema de avatares
"""
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'olhar_literario_django'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olhar_literario_django.settings')
django.setup()

from django.core.management import call_command
from django.db import connection

print("🔧 Aplicando migrations para novo sistema de avatares...")

# Primeiro, vamos fazer a migration manualmente via SQL
cursor = connection.cursor()

try:
    print("\n📋 Verificando estrutura atual da tabela books_userprofile...")
    cursor.execute("PRAGMA table_info(books_userprofile)")
    colunas = cursor.fetchall()
    
    tem_foto = any(col[1] == 'foto' for col in colunas)
    tem_avatar_tipo = any(col[1] == 'avatar_tipo' for col in colunas)
    tem_avatar_personalizado = any(col[1] == 'avatar_personalizado' for col in colunas)
    
    print(f"   - Coluna 'foto': {'✅ Existe' if tem_foto else '❌ Não existe'}")
    print(f"   - Coluna 'avatar_tipo': {'✅ Existe' if tem_avatar_tipo else '❌ Não existe'}")
    print(f"   - Coluna 'avatar_personalizado': {'✅ Existe' if tem_avatar_personalizado else '❌ Não existe'}")
    
    if tem_foto and not tem_avatar_tipo:
        print("\n🔨 Aplicando migration manualmente...")
        
        # Adicionar novos campos
        print("   1. Adicionando campo avatar_tipo...")
        cursor.execute("""
            ALTER TABLE books_userprofile 
            ADD COLUMN avatar_tipo VARCHAR(20) DEFAULT 'initials' NOT NULL
        """)
        
        print("   2. Adicionando campo avatar_personalizado...")
        cursor.execute("""
            ALTER TABLE books_userprofile 
            ADD COLUMN avatar_personalizado VARCHAR(100) NULL
        """)
        
        # Copiar dados de foto para avatar_personalizado
        print("   3. Migrando dados de 'foto' para 'avatar_personalizado'...")
        cursor.execute("""
            UPDATE books_userprofile 
            SET avatar_personalizado = foto, avatar_tipo = 'custom'
            WHERE foto IS NOT NULL AND foto != ''
        """)
        
        # Remover coluna antiga
        print("   4. Removendo coluna 'foto' antiga...")
        cursor.execute("""
            CREATE TABLE books_userprofile_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE REFERENCES auth_user(id),
                telefone VARCHAR(20) NULL,
                data_nascimento DATE NULL,
                bio TEXT NULL,
                avatar_personalizado VARCHAR(100) NULL,
                avatar_tipo VARCHAR(20) DEFAULT 'initials' NOT NULL
            )
        """)
        
        cursor.execute("""
            INSERT INTO books_userprofile_new 
            (id, user_id, telefone, data_nascimento, bio, avatar_personalizado, avatar_tipo)
            SELECT id, user_id, telefone, data_nascimento, bio, avatar_personalizado, avatar_tipo
            FROM books_userprofile
        """)
        
        cursor.execute("DROP TABLE books_userprofile")
        cursor.execute("ALTER TABLE books_userprofile_new RENAME TO books_userprofile")
        
        print("\n✅ Migration aplicada com sucesso!")
        
    elif tem_avatar_tipo:
        print("\n✅ Tabela já está atualizada!")
    else:
        print("\n⚠️ Estado inesperado da tabela. Executando makemigrations e migrate...")
        call_command('makemigrations')
        call_command('migrate')
        
except Exception as e:
    print(f"\n❌ Erro ao aplicar migration: {e}")
    import traceback
    traceback.print_exc()
    
    print("\n🔄 Tentando método alternativo...")
    try:
        call_command('makemigrations', 'books')
        call_command('migrate', 'books')
        print("✅ Migrations aplicadas via Django!")
    except Exception as e2:
        print(f"❌ Erro no método alternativo: {e2}")

print("\n🔍 Verificando estrutura final...")
cursor.execute("PRAGMA table_info(books_userprofile)")
colunas_final = cursor.fetchall()
print("\n📋 Colunas atuais em books_userprofile:")
for col in colunas_final:
    print(f"   - {col[1]} ({col[2]})")

print("\n✅ Processo finalizado!")
