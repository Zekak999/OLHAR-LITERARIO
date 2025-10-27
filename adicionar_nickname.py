"""
Script para adicionar campo 'nickname' na tabela books_userprofile
"""
import sqlite3
import os

# Caminho do banco de dados
db_path = os.path.join('olhar_literario_django', 'db.sqlite3')

if not os.path.exists(db_path):
    print(f"❌ Banco de dados não encontrado: {db_path}")
    exit(1)

# Conectar ao banco
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Verificar se a coluna já existe
    cursor.execute("PRAGMA table_info(books_userprofile)")
    colunas = [col[1] for col in cursor.fetchall()]
    
    if 'nickname' in colunas:
        print("✅ Campo 'nickname' já existe na tabela!")
    else:
        print("🔧 Adicionando campo 'nickname' na tabela books_userprofile...")
        
        # Adicionar coluna nickname
        cursor.execute("""
            ALTER TABLE books_userprofile 
            ADD COLUMN nickname VARCHAR(50)
        """)
        
        conn.commit()
        print("✅ Campo 'nickname' adicionado com sucesso!")
    
    # Verificar estrutura final
    cursor.execute("PRAGMA table_info(books_userprofile)")
    colunas_finais = cursor.fetchall()
    
    print("\n📊 Estrutura da tabela books_userprofile:")
    for col in colunas_finais:
        print(f"  - {col[1]} ({col[2]})")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    conn.rollback()
finally:
    conn.close()

print("\n✅ Script concluído!")
