"""
Comando Django para criar UserProfile para todos os usuários
Uso: python manage.py criar_user_profiles
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from books.models import UserProfile


class Command(BaseCommand):
    help = 'Cria UserProfile para todos os usuários que não têm'

    def handle(self, *args, **options):
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.WARNING('🔧 CRIANDO USERPROFILE PARA USUÁRIOS SEM PERFIL'))
        self.stdout.write("=" * 70)
        
        usuarios = User.objects.all()
        criados = 0
        ja_existentes = 0
        
        for usuario in usuarios:
            profile, created = UserProfile.objects.get_or_create(user=usuario)
            if created:
                criados += 1
                self.stdout.write(self.style.SUCCESS(f"✅ Profile criado para: {usuario.username}"))
            else:
                ja_existentes += 1
                self.stdout.write(f"ℹ️  Profile já existe para: {usuario.username}")
        
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.WARNING('📊 RESUMO:'))
        self.stdout.write(f"   • Total de usuários: {usuarios.count()}")
        self.stdout.write(self.style.SUCCESS(f"   • Profiles criados: {criados}"))
        self.stdout.write(f"   • Profiles já existentes: {ja_existentes}")
        self.stdout.write("=" * 70 + "\n")
        
        if criados > 0:
            self.stdout.write(self.style.SUCCESS(f'\n✅ {criados} profiles criados com sucesso!'))
        else:
            self.stdout.write(self.style.SUCCESS('\n✅ Todos os usuários já possuem profiles!'))
