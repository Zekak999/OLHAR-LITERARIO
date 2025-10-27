#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para popular o banco de dados PostgreSQL no Railway com livros
IMPORTANTE: Marca todos os livros como disponível=True e alguns em destaque
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olhar_literario_django.settings')
django.setup()

from books.models import Book

# Livros de exemplo - TODOS marcados como disponível e alguns em destaque
livros_exemplo = [
    {
        'titulo': 'Harry Potter e a Pedra Filosofal',
        'autor': 'J. K. Rowling',
        'editora': 'Rocco',
        'ano_publicacao': 2000,
        'isbn': '9788532530787',
        'genero': 'Fantasia',
        'sinopse': 'Harry Potter é um garoto órfão que vive infeliz com seus tios, os Dursleys. Aos 11 anos, ele recebe uma carta contendo um convite para ingressar em Hogwarts, uma escola para bruxos. A partir de então, Harry fica sabendo que é um bruxo e que seus pais foram assassinados por Voldemort.',
        'paginas': 264,
        'idioma': 'Português',
        'disponivel': True,
        'destaque': True,  # EM DESTAQUE
        'capa_url': 'https://m.media-amazon.com/images/I/81ibfYk4qmL._SY466_.jpg',
    },
    {
        'titulo': 'A Culpa é das Estrelas',
        'autor': 'John Green',
        'editora': 'Intrínseca',
        'ano_publicacao': 2012,
        'isbn': '9788580572261',
        'genero': 'Romance',
        'sinopse': 'Hazel é uma paciente terminal. Ainda que, por um milagre da medicina, seu tumor tenha encolhido bastante, ela sabe que faz parte dos efeitos colaterais do câncer. Foi assim que ela conheceu Augustus Waters, em um Grupo de Apoio para Crianças com Câncer.',
        'paginas': 288,
        'idioma': 'Português',
        'disponivel': True,
        'destaque': True,  # EM DESTAQUE
        'capa_url': 'https://m.media-amazon.com/images/I/71u5f1N3xCL._SY466_.jpg',
    },
    {
        'titulo': 'A Sutil Arte de Ligar o Foda-se',
        'autor': 'Mark Manson',
        'editora': 'Intrínseca',
        'ano_publicacao': 2016,
        'isbn': '9788551001523',
        'genero': 'Autoajuda',
        'sinopse': 'Chega de tentar buscar um sucesso que só existe na sua cabeça. Na contramão da autoajuda convencional, Mark Manson prova que a chave para pessoas mais confiantes e felizes é parar de fugir dos problemas e encarar as verdades dolorosas.',
        'paginas': 224,
        'idioma': 'Português',
        'disponivel': True,
        'destaque': True,  # EM DESTAQUE
        'capa_url': 'https://m.media-amazon.com/images/I/71QpmGcmjIL._SY466_.jpg',
    },
    {
        'titulo': '1984',
        'autor': 'George Orwell',
        'editora': 'Companhia das Letras',
        'ano_publicacao': 1949,
        'isbn': '9788535914849',
        'genero': 'Distopia',
        'sinopse': 'Winston Smith trabalha para o Ministério da Verdade em Londres. É encarregado de reescrever a história para que sempre se adeque à linha partidária contemporânea. O Partido controla tudo na Oceânia, até mesmo os pensamentos das pessoas.',
        'paginas': 416,
        'idioma': 'Português',
        'disponivel': True,
        'destaque': True,  # EM DESTAQUE
        'capa_url': 'https://m.media-amazon.com/images/I/819js3EQwbL._SY466_.jpg',
    },
    {
        'titulo': 'O Hobbit',
        'autor': 'J. R. R. Tolkien',
        'editora': 'HarperCollins',
        'ano_publicacao': 1937,
        'isbn': '9788595084742',
        'genero': 'Fantasia',
        'sinopse': 'Como a maioria dos hobbits, Bilbo Bolseiro leva uma vida tranquila até o dia em que recebe uma missão do mago Gandalf. Acompanhado por um grupo de anões, ele precisa viajar até a Montanha Solitária para libertar o Reino de Erebor do dragão Smaug.',
        'paginas': 336,
        'idioma': 'Português',
        'disponivel': True,
        'destaque': True,  # EM DESTAQUE
        'capa_url': 'https://m.media-amazon.com/images/I/91M9xPIf10L._SY466_.jpg',
    },
    {
        'titulo': 'O Pequeno Príncipe',
        'autor': 'Antoine de Saint-Exupéry',
        'editora': 'Agir',
        'ano_publicacao': 1943,
        'isbn': '9788522008728',
        'genero': 'Fábula',
        'sinopse': 'Nesta clássica história de amor e amizade, um piloto cai com seu avião no deserto do Saara e encontra um pequeno príncipe vindo de outro planeta. As lições ensinadas pelo príncipe sobre amor, amizade e valores humanos tocam o coração de leitores de todas as idades.',
        'paginas': 96,
        'idioma': 'Português',
        'disponivel': True,
        'destaque': True,  # EM DESTAQUE
        'capa_url': 'https://m.media-amazon.com/images/I/71OZY035lkL._SY466_.jpg',
    },
    {
        'titulo': 'Dom Casmurro',
        'autor': 'Machado de Assis',
        'editora': 'Penguin-Companhia',
        'ano_publicacao': 1899,
        'isbn': '9788563560278',
        'genero': 'Romance',
        'sinopse': 'Bentinho e Capitu são amigos de infância. Ela, menina esperta e vivaz. Ele, jovem ingênuo que vai estudar para ser padre. Um amor impossível nasce entre eles, gerando uma história de amor, ciúmes e traição que atravessa gerações.',
        'paginas': 256,
        'idioma': 'Português',
        'disponivel': True,
        'destaque': False,
        'capa_url': 'https://m.media-amazon.com/images/I/71dqRJk+GjL._SY466_.jpg',
    },
    {
        'titulo': 'O Senhor dos Anéis: A Sociedade do Anel',
        'autor': 'J. R. R. Tolkien',
        'editora': 'HarperCollins',
        'ano_publicacao': 1954,
        'isbn': '9788595084759',
        'genero': 'Fantasia',
        'sinopse': 'Em uma terra fantástica chamada Terra-média, o hobbit Frodo Bolseiro herda um Anel mágico de seu tio Bilbo. O mago Gandalf descobre que este é o Um Anel, a arma definitiva do Senhor do Escuro Sauron, que busca controlar a Terra-média.',
        'paginas': 576,
        'idioma': 'Português',
        'disponivel': True,
        'destaque': False,
        'capa_url': 'https://m.media-amazon.com/images/I/81hCVEC0ExL._SY466_.jpg',
    },
]

def popular_livros():
    """Adiciona os livros de exemplo ao banco de dados"""
    print("="*70)
    print("🔄 POPULANDO BANCO DE DADOS COM LIVROS")
    print("="*70)
    
    # Mostrar qual banco está sendo usado
    from django.conf import settings
    db_config = settings.DATABASES['default']
    if 'postgresql' in db_config.get('ENGINE', ''):
        print("🔵 Banco: PostgreSQL (Produção/Railway)")
    else:
        print("🟡 Banco: SQLite (Local)")
    print("="*70)
    print()
    
    livros_criados = 0
    livros_existentes = 0
    livros_atualizados = 0
    
    for livro_data in livros_exemplo:
        titulo = livro_data['titulo']
        
        # Verificar se o livro já existe
        livro_existente = Book.objects.filter(titulo=titulo).first()
        
        if livro_existente:
            # Atualizar disponivel e destaque se necessário
            atualizado = False
            if not livro_existente.disponivel:
                livro_existente.disponivel = True
                atualizado = True
            if livro_data.get('destaque', False) and not livro_existente.destaque:
                livro_existente.destaque = True
                atualizado = True
            if livro_data.get('capa_url') and not livro_existente.capa_url:
                livro_existente.capa_url = livro_data.get('capa_url')
                atualizado = True
                
            if atualizado:
                livro_existente.save()
                print(f"🔄 '{titulo}' atualizado (disponível/destaque)")
                livros_atualizados += 1
            else:
                print(f"⏭️  '{titulo}' já existe")
                livros_existentes += 1
            continue
        
        # Criar o livro
        try:
            livro = Book.objects.create(**livro_data)
            destaque_str = " ⭐ DESTAQUE" if livro_data.get('destaque', False) else ""
            print(f"✅ '{livro.titulo}' criado{destaque_str}")
            livros_criados += 1
        except Exception as e:
            print(f"❌ Erro ao criar '{titulo}': {e}")
    
    print()
    print("="*70)
    print(f"📚 RESUMO:")
    print(f"   ✅ Livros criados: {livros_criados}")
    print(f"   🔄 Livros atualizados: {livros_atualizados}")
    print(f"   ⏭️  Livros já existentes: {livros_existentes}")
    print(f"   📖 TOTAL no banco: {Book.objects.count()}")
    print(f"   ⭐ Livros em DESTAQUE: {Book.objects.filter(destaque=True).count()}")
    print(f"   ✔️  Livros DISPONÍVEIS: {Book.objects.filter(disponivel=True).count()}")
    print("="*70)
    print()
    print("✨ Pronto! Os livros estão disponíveis no site!")
    print("🌐 Acesse: /admin/ para gerenciar")
    print("🏠 Acesse: / para ver os livros")
    print()

if __name__ == '__main__':
    popular_livros()
