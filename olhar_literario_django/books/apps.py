from django.apps import AppConfig


class BooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'books'
    verbose_name = 'Olhar Literário - Sistema de Livros'
    
    def ready(self):
        """
        Executado quando o Django inicia.
        Importa os signals e cria o superusuário automaticamente se não existir.
        """
        # Importar signals para criar UserProfile automaticamente
        import books.signals
        
        # Só executar em produção (quando DEBUG=False)
        from django.conf import settings
        if not settings.DEBUG:
            self.criar_superusuario()
    
    def criar_superusuario(self):
        """Cria superusuário admin/admin123 automaticamente"""
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            username = 'admin'
            password = 'admin123'
            email = 'admin@olharliterario.com'
            
            print("\n" + "=" * 70)
            print("🚀 AUTO-CRIAÇÃO DE SUPERUSUÁRIO (via apps.py)")
            print("=" * 70)
            
            # Verificar se já existe - NÃO DELETAR!
            if User.objects.filter(username=username).exists():
                print(f"✅ Usuário '{username}' já existe")
                print("=" * 70 + "\n")
                return
            
            # Criar novo superusuário
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            
            print("=" * 70)
            print("✅ ✅ ✅ SUPERUSUÁRIO CRIADO COM SUCESSO! ✅ ✅ ✅")
            print("=" * 70)
            print(f"👤 Username: {username}")
            print(f"🔑 Senha: {password}")
            print(f"⭐ is_superuser: {user.is_superuser}")
            print(f"👔 is_staff: {user.is_staff}")
            print("=" * 70 + "\n")
            
        except Exception as e:
            print("\n" + "=" * 70)
            print(f"⚠️  Erro ao criar superusuário: {e}")
            print("=" * 70 + "\n")
            # Não fazer raise para não quebrar o startup do Django

