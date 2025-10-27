import sqlite3
import os

# Caminho do banco de dados
db_path = os.path.join('olhar_literario_django', 'db.sqlite3')

print(f"🔧 Aplicando migration no banco: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Verificar estrutura atual
    print("\n📋 Verificando estrutura atual...")
    cursor.execute("PRAGMA table_info(books_userprofile)")
    colunas = {col[1]: col[2] for col in cursor.fetchall()}
    
    print(f"   Colunas encontradas: {list(colunas.keys())}")
    
    tem_foto = 'foto' in colunas
    tem_avatar_tipo = 'avatar_tipo' in colunas
    
    if tem_foto and not tem_avatar_tipo:
        print("\n🔨 Aplicando migration...")
        
        # Passo 1: Adicionar novos campos
        print("   1. Adicionando campo avatar_tipo...")
        try:
            cursor.execute("ALTER TABLE books_userprofile ADD COLUMN avatar_tipo VARCHAR(20) DEFAULT 'initials'")
        except sqlite3.OperationalError as e:
            if "duplicate column" not in str(e).lower():
                raise
            print("      (Campo já existe)")
        
        print("   2. Adicionando campo avatar_personalizado...")
        try:
            cursor.execute("ALTER TABLE books_userprofile ADD COLUMN avatar_personalizado VARCHAR(100)")
        except sqlite3.OperationalError as e:
            if "duplicate column" not in str(e).lower():
                raise
            print("      (Campo já existe)")
        
        conn.commit()
        
        # Passo 2: Migrar dados
        print("   3. Migrando dados de 'foto' para 'avatar_personalizado'...")
        cursor.execute("""
            UPDATE books_userprofile 
            SET avatar_personalizado = foto,
                avatar_tipo = 'custom'
            WHERE foto IS NOT NULL AND foto != ''
        """)
        conn.commit()
        
        # Passo 3: Recriar tabela sem campo 'foto'
        print("   4. Recriando tabela sem campo 'foto'...")
        
        cursor.execute("""
            CREATE TABLE books_userprofile_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED,
                telefone VARCHAR(20),
                data_nascimento DATE,
                bio TEXT,
                avatar_personalizado VARCHAR(100),
                avatar_tipo VARCHAR(20) DEFAULT 'initials' NOT NULL
            )
        """)
        
        cursor.execute("""
            INSERT INTO books_userprofile_new 
            (id, user_id, telefone, data_nascimento, bio, avatar_personalizado, avatar_tipo)
            SELECT id, user_id, telefone, data_nascimento, bio, 
                   avatar_personalizado, 
                   COALESCE(avatar_tipo, 'initials')
            FROM books_userprofile
        """)
        
        cursor.execute("DROP TABLE books_userprofile")
        cursor.execute("ALTER TABLE books_userprofile_new RENAME TO books_userprofile")
        
        conn.commit()
        print("\n✅ Migration aplicada com sucesso!")
        
    elif tem_avatar_tipo:
        print("\n✅ Tabela já está atualizada!")
    else:
        print("\n⚠️ Estado inesperado da tabela")
    
    # Verificar resultado final
    print("\n🔍 Estrutura final:")
    cursor.execute("PRAGMA table_info(books_userprofile)")
    for col in cursor.fetchall():
        print(f"   - {col[1]} ({col[2]})")
    
    conn.close()
    print("\n✅ Processo concluído!")
    
except Exception as e:
    print(f"\n❌ Erro: {e}")
    import traceback
    traceback.print_exc()
