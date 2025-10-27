#!/usr/bin/env python
"""Script para criar um livro de teste no banco de dados"""
import sqlite3
from datetime import datetime

# Conectar ao banco SQLite
db_path = r'C:\Users\zekak\Desktop\olharliterario-master\olharliterario-master\olhar_literario_django\db.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Dados do livro de teste
    livro = {
        'titulo': 'O Senhor dos Anéis: A Sociedade do Anel',
        'autor': 'J.R.R. Tolkien',
        'editora': 'HarperCollins',
        'ano_publicacao': 1954,
        'isbn': '9780261102385',
        'genero': 'Fantasia',
        'sinopse': 'Em uma terra fantástica e única, um hobbit recebe de presente de seu tio um anel mágico e maligno que precisa ser destruído antes que caia nas mãos do mal. Para isso, o hobbit Frodo terá a ajuda de uma Sociedade do Anel, formada por pessoas e seres de diferentes raças.',
        'capa_url': 'https://m.media-amazon.com/images/I/81hCVEC0ExL._SY522_.jpg',
        'paginas': 576,
        'idioma': 'Português',
        'disponivel': 1,
        'destaque': 1,
        'data_cadastro': datetime.now().isoformat()
    }
    
    # Inserir livro
    cursor.execute("""
        INSERT INTO books_book (
            titulo, autor, editora, ano_publicacao, isbn, genero, sinopse,
            capa_url, capa, paginas, idioma, disponivel, destaque, data_cadastro
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, '', ?, ?, ?, ?, ?
        )
    """, (
        livro['titulo'],
        livro['autor'],
        livro['editora'],
        livro['ano_publicacao'],
        livro['isbn'],
        livro['genero'],
        livro['sinopse'],
        livro['capa_url'],
        livro['paginas'],
        livro['idioma'],
        livro['disponivel'],
        livro['destaque'],
        livro['data_cadastro']
    ))
    
    livro_id = cursor.lastrowid
    
    # Criar alguns comentários de teste
    comentarios = [
        {
            'usuario': 'zekak@zekak.com',
            'texto': 'Obra-prima da fantasia! A construção do mundo da Terra Média é incrível.',
            'avaliacao': 5
        },
        {
            'usuario': 'admin@olharliterario.com',
            'texto': 'Um clássico que nunca envelhece. Leitura obrigatória!',
            'avaliacao': 5
        },
        {
            'usuario': 'leitor@teste.com',
            'texto': 'Muito bom, mas achei o ritmo um pouco lento em alguns momentos.',
            'avaliacao': 4
        }
    ]
    
    for comentario in comentarios:
        cursor.execute("""
            INSERT INTO books_comment (
                book_title, user_id, comentario, avaliacao, data_comentario, book_id
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            livro['titulo'],
            comentario['usuario'],
            comentario['texto'],
            comentario['avaliacao'],
            datetime.now().isoformat(),
            livro_id
        ))
    
    conn.commit()
    
    print("=" * 60)
    print("✅ LIVRO DE TESTE CRIADO COM SUCESSO!")
    print("=" * 60)
    print(f"📚 Título: {livro['titulo']}")
    print(f"✍️  Autor: {livro['autor']}")
    print(f"📖 Gênero: {livro['genero']}")
    print(f"⭐ Avaliações: 3 comentários adicionados")
    print(f"🎯 ID do livro: {livro_id}")
    print("=" * 60)
    print(f"🌐 Acesse: http://localhost:8000/livro.html?id={livro_id}")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Erro: {e}")
    conn.rollback()
finally:
    conn.close()
