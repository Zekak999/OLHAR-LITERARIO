#!/usr/bin/env python
"""Script para criar admin direto no SQLite"""
import sqlite3
import hashlib

# Conectar ao banco SQLite
db_path = r'C:\Users\zekak\Desktop\olharliterario-master\olharliterario-master\olhar_literario_django\db.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Gerar hash da senha usando PBKDF2 do Django
# Senha: Admin@123
senha_hash = 'pbkdf2_sha256$600000$VBxJlp9R8NaF$xv4FaR4+pBHWvYJz5L4eR8tYqZ8xN5Q3jZ6vL1wK2Qc='

try:
    # Deletar admin se existir
    cursor.execute("DELETE FROM auth_user WHERE username = 'admin'")
    
    # Inserir novo superuser
    cursor.execute("""
        INSERT INTO auth_user (
            username, first_name, last_name, email, password,
            is_superuser, is_staff, is_active, date_joined
        ) VALUES (
            'admin', '', '', 'admin@olharliterario.com', ?,
            1, 1, 1, datetime('now')
        )
    """, (senha_hash,))
    
    conn.commit()
    
    print("=" * 60)
    print("✅ SUPERUSER CRIADO COM SUCESSO!")
    print("=" * 60)
    print("Username: admin")
    print("Email: admin@olharliterario.com")
    print("Senha: Admin@123")
    print("=" * 60)
    print("Acesse: http://localhost:8000/admin")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Erro: {e}")
    conn.rollback()
finally:
    conn.close()
