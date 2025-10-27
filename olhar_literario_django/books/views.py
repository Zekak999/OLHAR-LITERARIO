from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
import json
import uuid
import os
from pathlib import Path
from .models import UserProfile, AuthToken, Comment, Book


# Diretório base para arquivos estáticos
BASE_DIR = Path(__file__).resolve().parent.parent.parent


def health_check(request):
    """Health check para verificar se o servidor está funcionando"""
    from django.db import connection
    
    # Testar conexão com banco de dados
    db_status = "disconnected"
    db_type = "unknown"
    try:
        connection.ensure_connection()
        db_status = "connected"
        db_type = connection.settings_dict['ENGINE'].split('.')[-1]
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return JsonResponse({
        'status': 'ok',
        'message': 'Django está funcionando!',
        'debug': settings.DEBUG,
        'database': {
            'type': db_type,
            'status': db_status
        },
        'templates_dir': str(settings.BASE_DIR / 'templates')
    })


def index_view(request):
    """Serve a página inicial do site"""
    return render(request, 'index.html')


def livro_view(request):
    """Serve a página de detalhes do livro"""
    return render(request, 'livro.html')


def biblioteca_view(request):
    """Serve a página da biblioteca"""
    return render(request, 'biblioteca.html')


def perfil_view(request):
    """Serve a página de perfil do usuário"""
    return render(request, 'perfil.html')


def login_view(request):
    """Serve a página de login"""
    return render(request, 'login.html')


def registro_view(request):
    """Serve a página de registro"""
    return render(request, 'registro.html')


def get_user_from_token(request):
    """
    Extrai e valida o token de autenticação do header Authorization
    Retorna o usuário autenticado ou None
    """
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None
    
    token_string = auth_header.split(' ', 1)[1]
    try:
        token = AuthToken.objects.select_related('user').get(token=token_string)
        if token.is_valid():
            return token.user
    except AuthToken.DoesNotExist:
        pass
    
    return None


def auth_required(view_func):
    """Decorator para proteger views que requerem autenticação"""
    def wrapper(request, *args, **kwargs):
        user = get_user_from_token(request)
        if not user:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        request.authenticated_user = user
        return view_func(request, *args, **kwargs)
    return wrapper


@csrf_exempt
@require_http_methods(["POST"])
def api_register(request):
    """Registra um novo usuário"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    data_nascimento = data.get('dataNascimento')
    
    # Validar campos obrigatórios
    if not nome:
        return JsonResponse({'error': 'Nome é obrigatório'}, status=400)
    if not email:
        return JsonResponse({'error': 'Email é obrigatório'}, status=400)
    if not senha:
        return JsonResponse({'error': 'Senha é obrigatória'}, status=400)
    
    # Validar email
    if '@' not in email:
        return JsonResponse({'error': 'Email inválido'}, status=400)
    
    # Verificar se email já existe
    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'Este email já está cadastrado'}, status=400)
    
    # Verificar se username (email) já existe
    if User.objects.filter(username=email).exists():
        return JsonResponse({'error': 'Este email já está cadastrado'}, status=400)
    
    # Criar usuário
    try:
        user = User.objects.create(
            username=email,  # Usar email como username
            email=email,
            first_name=nome,
            password=make_password(senha)
        )
        
        # Criar perfil
        profile = UserProfile.objects.create(
            user=user,
            data_nascimento=data_nascimento if data_nascimento else None
        )
        
        # Criar token
        token = AuthToken.objects.create(user=user)
        
        return JsonResponse({
            'user': {
                'id': user.id,
                'nome': nome,
                'email': email
            },
            'token': token.token
        })
    except Exception as e:
        return JsonResponse({'error': f'Erro ao criar usuário: {str(e)}'}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    """Faz login do usuário"""
    try:
        data = json.loads(request.body)
        print(f"Login attempt - Data received: {data}")
    except json.JSONDecodeError as e:
        print(f"Login error - Invalid JSON: {e}")
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    email = data.get('email')
    senha = data.get('senha')
    
    print(f"Login attempt - Email: {email}, Password provided: {'Yes' if senha else 'No'}")
    
    if not all([email, senha]):
        print(f"Login error - Missing fields. Email: {email}, Senha: {'provided' if senha else 'missing'}")
        return JsonResponse({'error': 'Email e senha são obrigatórios'}, status=400)
    
    try:
        user = User.objects.get(email=email)
        print(f"User found: {user.username}, checking password...")
        if check_password(senha, user.password):
            print(f"Password correct, creating token...")
            # Criar novo token
            token = AuthToken.objects.create(user=user)
            
            return JsonResponse({
                'user': {
                    'id': user.id,
                    'nome': user.first_name,
                    'email': user.email
                },
                'token': token.token
            })
        else:
            print(f"Password incorrect for user: {user.username}")
            return JsonResponse({'error': 'Email ou senha incorretos'}, status=400)
    except User.DoesNotExist:
        print(f"User not found with email: {email}")
        return JsonResponse({'error': 'Email ou senha incorretos'}, status=400)


@csrf_exempt
@require_http_methods(["GET", "POST"])
@auth_required
def api_profile(request):
    """Obtém ou atualiza perfil do usuário"""
    user = request.authenticated_user
    
    if request.method == 'GET':
        # Obter perfil
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)
        
        # Retornar avatar usando o novo método
        avatar_url = None
        avatar_tipo = 'initials'
        if profile:
            try:
                avatar_url = profile.get_avatar_url()
                avatar_tipo = profile.avatar_tipo
            except Exception as e:
                print(f"⚠️ Erro ao obter avatar: {e}")
                # Fallback para iniciais
                nome = user.first_name or user.username
                iniciais = ''.join([c[0].upper() for c in nome.split()[:2]])
                if not iniciais:
                    iniciais = user.username[0].upper()
                avatar_url = f"https://ui-avatars.com/api/?name={iniciais}&background=4A90E2&color=fff&size=200&bold=true"
        
        return JsonResponse({
            'id': user.id,
            'nome': user.first_name,
            'email': user.email,
            'dataNascimento': profile.data_nascimento.isoformat() if profile.data_nascimento else None,
            'telefone': profile.telefone or '',
            'bio': profile.bio or '',
            'foto': avatar_url,
            'avatar_tipo': avatar_tipo,
            'is_superuser': user.is_superuser
        })
    
    elif request.method == 'POST':
        # Atualizar perfil
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        nome = data.get('nome')
        telefone = data.get('telefone')
        bio = data.get('bio')
        data_nascimento = data.get('dataNascimento')
        
        # Atualizar usuário
        if nome:
            user.first_name = nome
            user.save()
        
        # Atualizar perfil
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)
        
        if telefone is not None:
            profile.telefone = telefone
        if bio is not None:
            profile.bio = bio
        if data_nascimento:
            profile.data_nascimento = data_nascimento
        
        profile.save()
        
        return JsonResponse({'success': True})


@csrf_exempt
@require_http_methods(["POST"])
@auth_required
def api_upload_photo(request):
    """Upload de avatar personalizado"""
    user = request.authenticated_user
    
    print(f"📸 Upload de avatar - Usuário: {user.username}")
    print(f"📋 FILES: {request.FILES}")
    print(f"📋 POST: {request.POST}")
    
    if 'file' not in request.FILES:
        print("❌ Erro: 'file' não encontrado em request.FILES")
        return JsonResponse({'error': 'No file provided'}, status=400)
    
    file = request.FILES['file']
    print(f"📁 Arquivo recebido: {file.name} - Tamanho: {file.size} bytes")
    
    # Validar tipo de arquivo
    allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
    if file.content_type not in allowed_types:
        return JsonResponse({'error': 'Tipo de arquivo não permitido. Use JPG, PNG, GIF ou WebP'}, status=400)
    
    # Validar tamanho (máximo 5MB)
    if file.size > 5 * 1024 * 1024:
        return JsonResponse({'error': 'Arquivo muito grande. Máximo 5MB'}, status=400)
    
    if not file.name:
        print("❌ Erro: Nome do arquivo vazio")
        return JsonResponse({'error': 'No filename'}, status=400)
    
    # Obter ou criar perfil
    try:
        profile = user.profile
        print(f"✅ Perfil encontrado: {profile}")
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
        print(f"✅ Perfil criado: {profile}")
    
    # Salvar arquivo
    try:
        # Deletar avatar antigo se existir
        if profile.avatar_personalizado:
            try:
                profile.avatar_personalizado.delete(save=False)
                print("🗑️ Avatar antigo deletado")
            except:
                pass
        
        profile.avatar_personalizado = file
        profile.avatar_tipo = 'custom'
        profile.save()
        
        avatar_url = profile.get_avatar_url()
        print(f"✅ Avatar salvo com sucesso!")
        print(f"📂 URL do avatar: {avatar_url}")
        
        return JsonResponse({
            'avatar': avatar_url,
            'tipo': 'custom',
            'message': 'Avatar atualizado com sucesso!'
        })
    except Exception as e:
        print(f"❌ Erro ao salvar avatar: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': f'Erro ao salvar: {str(e)}'}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_change_avatar_type(request):
    """Mudar tipo de avatar (iniciais, dicebear, custom)"""
    user = get_user_from_token(request)
    if not user:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    try:
        data = json.loads(request.body)
        tipo = data.get('tipo', 'initials')
        
        if tipo not in ['initials', 'dicebear', 'custom']:
            return JsonResponse({'error': 'Tipo inválido'}, status=400)
        
        # Obter ou criar perfil
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)
        
        # Se mudar para custom mas não tem foto, usar iniciais
        if tipo == 'custom' and not profile.avatar_personalizado:
            tipo = 'initials'
        
        profile.avatar_tipo = tipo
        profile.save()
        
        avatar_url = profile.get_avatar_url()
        
        return JsonResponse({
            'avatar': avatar_url,
            'tipo': tipo,
            'message': 'Tipo de avatar atualizado!'
        })
    except Exception as e:
        print(f"❌ Erro ao trocar tipo de avatar: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_comments(request):
    """Obtém ou cria comentários"""
    if request.method == 'POST':
        # Criar comentário (requer autenticação)
        user = get_user_from_token(request)
        if not user:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        book_title = data.get('book_title')
        comment_text = data.get('comment')
        rating = data.get('rating', 0)
        
        if not all([book_title, comment_text, rating]):
            return JsonResponse({'error': 'Missing fields'}, status=400)
        
        try:
            # Buscar o livro pelo título para vincular corretamente
            try:
                book = Book.objects.get(titulo__iexact=book_title)
            except Book.DoesNotExist:
                book = None
            
            comment = Comment.objects.create(
                user=user,
                book=book,  # Vincular à ForeignKey
                book_title=book_title,
                comment=comment_text,
                rating=int(rating)
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif request.method == 'GET':
        # Obter comentários
        book = request.GET.get('book')
        
        if book:
            comments = Comment.objects.filter(book_title=book).select_related('user')
        else:
            comments = Comment.objects.all().select_related('user')
        
        comments_data = []
        for comment in comments:
            comments_data.append({
                'id': comment.id,
                'user_id': comment.user.id,
                'user_nome': comment.user.first_name or comment.user.username,
                'book_title': comment.book_title,
                'comment': comment.comment,
                'rating': comment.rating,
                'created_at': comment.created_at.isoformat()
            })
        
        return JsonResponse(comments_data, safe=False)


@csrf_exempt
@require_http_methods(["DELETE"])
def api_delete_comment(request, comment_id):
    """Deleta um comentário (apenas o próprio usuário pode deletar)"""
    user = get_user_from_token(request)
    if not user:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    try:
        comment = Comment.objects.get(id=comment_id)
        
        # Verificar se o comentário pertence ao usuário
        if comment.user.id != user.id:
            return JsonResponse({'error': 'Você não tem permissão para deletar este comentário'}, status=403)
        
        comment.delete()
        return JsonResponse({'success': True, 'message': 'Comentário deletado com sucesso'})
    
    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Comentário não encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def api_books(request):
    """Obtém lista de livros cadastrados"""
    # Filtros opcionais
    book_id = request.GET.get('id')
    genero = request.GET.get('genero')
    autor = request.GET.get('autor')
    editora = request.GET.get('editora')
    busca = request.GET.get('q')
    titulo = request.GET.get('titulo')
    disponivel = request.GET.get('disponivel')
    destaque = request.GET.get('destaque')
    
    # Query base
    books = Book.objects.filter(disponivel=True)
    
    # Aplicar filtros
    if book_id:
        books = books.filter(id=book_id)
    if titulo:
        books = books.filter(titulo__iexact=titulo)
    if genero:
        books = books.filter(genero__icontains=genero)
    if autor:
        books = books.filter(autor__icontains=autor)
    if editora:
        books = books.filter(editora__icontains=editora)
    if busca:
        books = books.filter(titulo__icontains=busca) | books.filter(autor__icontains=busca)
    if disponivel is not None:
        books = books.filter(disponivel=disponivel.lower() == 'true')
    if destaque is not None:
        books = books.filter(destaque=destaque.lower() == 'true')
    
    # Ordenar por destaque primeiro, depois por mais recentes
    books = books.order_by('-destaque', '-data_cadastro')
    
    # Construir resposta
    books_data = []
    for book in books:
        books_data.append({
            'id': book.id,
            'titulo': book.titulo,
            'autor': book.autor,
            'editora': book.editora or '',
            'ano_publicacao': book.ano_publicacao,
            'isbn': book.isbn or '',
            'genero': book.genero or '',
            'sinopse': book.sinopse or '',
            'capa': book.get_capa_url(),
            'paginas': book.paginas,
            'idioma': book.idioma,
            'disponivel': book.disponivel,
            'media_avaliacoes': round(book.media_avaliacoes(), 1),
            'total_avaliacoes': book.total_avaliacoes()
        })
    
    return JsonResponse(books_data, safe=False)
