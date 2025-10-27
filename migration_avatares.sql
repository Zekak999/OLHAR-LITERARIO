-- Migration SQL para novo sistema de avatares
-- Execute este script no banco de dados SQLite

-- 1. Verificar estrutura atual
.schema books_userprofile

-- 2. Adicionar novos campos
ALTER TABLE books_userprofile ADD COLUMN avatar_tipo VARCHAR(20) DEFAULT 'initials';
ALTER TABLE books_userprofile ADD COLUMN avatar_personalizado VARCHAR(100);

-- 3. Migrar dados de foto para avatar_personalizado
UPDATE books_userprofile 
SET avatar_personalizado = foto, 
    avatar_tipo = 'custom'
WHERE foto IS NOT NULL AND foto != '';

-- 4. Criar nova tabela sem o campo foto
CREATE TABLE books_userprofile_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED,
    telefone VARCHAR(20),
    data_nascimento DATE,
    bio TEXT,
    avatar_personalizado VARCHAR(100),
    avatar_tipo VARCHAR(20) DEFAULT 'initials' NOT NULL
);

-- 5. Copiar dados
INSERT INTO books_userprofile_new (id, user_id, telefone, data_nascimento, bio, avatar_personalizado, avatar_tipo)
SELECT id, user_id, telefone, data_nascimento, bio, avatar_personalizado, COALESCE(avatar_tipo, 'initials')
FROM books_userprofile;

-- 6. Substituir tabela
DROP TABLE books_userprofile;
ALTER TABLE books_userprofile_new RENAME TO books_userprofile;

-- 7. Verificar resultado
.schema books_userprofile
SELECT * FROM books_userprofile;
