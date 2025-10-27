# Script Python para popular livros no Railway via shell
# Cole este código no Railway Shell ou execute: python manage.py shell < popular_railway_shell.py

from books.models import Book

livros = [
    {'titulo': 'Harry Potter e a Pedra Filosofal', 'autor': 'J. K. Rowling', 'editora': 'Rocco', 'ano_publicacao': 2000, 'isbn': '9788532530787', 'genero': 'Fantasia', 'sinopse': 'Harry Potter é um garoto órfão que descobre ser um bruxo aos 11 anos.', 'paginas': 264, 'idioma': 'Português', 'disponivel': True, 'destaque': True, 'capa_url': 'https://m.media-amazon.com/images/I/81ibfYk4qmL._SY466_.jpg'},
    {'titulo': 'A Culpa é das Estrelas', 'autor': 'John Green', 'editora': 'Intrínseca', 'ano_publicacao': 2012, 'isbn': '9788580572261', 'genero': 'Romance', 'sinopse': 'Hazel conhece Augustus em um Grupo de Apoio para Crianças com Câncer.', 'paginas': 288, 'idioma': 'Português', 'disponivel': True, 'destaque': True, 'capa_url': 'https://m.media-amazon.com/images/I/71u5f1N3xCL._SY466_.jpg'},
    {'titulo': 'A Sutil Arte de Ligar o Foda-se', 'autor': 'Mark Manson', 'editora': 'Intrínseca', 'ano_publicacao': 2016, 'isbn': '9788551001523', 'genero': 'Autoajuda', 'sinopse': 'Mark Manson prova que a chave para ser feliz é parar de fugir dos problemas.', 'paginas': 224, 'idioma': 'Português', 'disponivel': True, 'destaque': True, 'capa_url': 'https://m.media-amazon.com/images/I/71QpmGcmjIL._SY466_.jpg'},
    {'titulo': '1984', 'autor': 'George Orwell', 'editora': 'Companhia das Letras', 'ano_publicacao': 1949, 'isbn': '9788535914849', 'genero': 'Distopia', 'sinopse': 'Winston Smith trabalha para o Ministério da Verdade reescrevendo a história.', 'paginas': 416, 'idioma': 'Português', 'disponivel': True, 'destaque': True, 'capa_url': 'https://m.media-amazon.com/images/I/819js3EQwbL._SY466_.jpg'},
    {'titulo': 'O Hobbit', 'autor': 'J. R. R. Tolkien', 'editora': 'HarperCollins', 'ano_publicacao': 1937, 'isbn': '9788595084742', 'genero': 'Fantasia', 'sinopse': 'Bilbo Bolseiro recebe uma missão de Gandalf para libertar Erebor do dragão Smaug.', 'paginas': 336, 'idioma': 'Português', 'disponivel': True, 'destaque': True, 'capa_url': 'https://m.media-amazon.com/images/I/91M9xPIf10L._SY466_.jpg'},
    {'titulo': 'O Pequeno Príncipe', 'autor': 'Antoine de Saint-Exupéry', 'editora': 'Agir', 'ano_publicacao': 1943, 'isbn': '9788522008728', 'genero': 'Fábula', 'sinopse': 'Um piloto cai no deserto e encontra um pequeno príncipe vindo de outro planeta.', 'paginas': 96, 'idioma': 'Português', 'disponivel': True, 'destaque': True, 'capa_url': 'https://m.media-amazon.com/images/I/71OZY035lkL._SY466_.jpg'},
]

print("="*70)
print("🔄 Populando banco PostgreSQL no Railway...")
print("="*70)

criados = 0
existentes = 0

for livro_data in livros:
    if Book.objects.filter(titulo=livro_data['titulo']).exists():
        print(f"⏭️  '{livro_data['titulo']}' já existe")
        existentes += 1
    else:
        Book.objects.create(**livro_data)
        print(f"✅ '{livro_data['titulo']}' criado ⭐")
        criados += 1

print("="*70)
print(f"📚 Criados: {criados} | Existentes: {existentes}")
print(f"📖 TOTAL: {Book.objects.count()} livros")
print(f"⭐ DESTAQUE: {Book.objects.filter(destaque=True).count()} livros")
print("="*70)
print("✅ Pronto! Livros disponíveis no site!")
