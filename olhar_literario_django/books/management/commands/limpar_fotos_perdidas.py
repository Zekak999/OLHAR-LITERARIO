from django.core.management.base import BaseCommand
from books.models import UserProfile
import os


class Command(BaseCommand):
    help = 'Limpa referências de fotos de perfil que não existem no disco'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Verificando fotos de perfil...\n')
        
        perfis_atualizados = 0
        
        for perfil in UserProfile.objects.all():
            if perfil.foto:
                try:
                    # Verificar se o arquivo existe
                    caminho_completo = perfil.foto.path
                    if not os.path.exists(caminho_completo):
                        self.stdout.write(
                            self.style.WARNING(f"❌ Foto não encontrada: {perfil.foto.name}")
                        )
                        self.stdout.write(f"   Usuário: {perfil.user.username}")
                        
                        # Limpar referência
                        perfil.foto = None
                        perfil.save()
                        perfis_atualizados += 1
                        self.stdout.write(self.style.SUCCESS("   ✅ Referência removida\n"))
                    else:
                        self.stdout.write(
                            self.style.SUCCESS(f"✅ Foto OK: {perfil.foto.name} - Usuário: {perfil.user.username}")
                        )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"❌ Erro ao verificar {perfil.user.username}: {str(e)}")
                    )
                    # Limpar referência em caso de erro
                    perfil.foto = None
                    perfil.save()
                    perfis_atualizados += 1
        
        if perfis_atualizados > 0:
            self.stdout.write(
                self.style.SUCCESS(f"\n🎉 {perfis_atualizados} perfil(is) atualizado(s)")
            )
        else:
            self.stdout.write(self.style.SUCCESS("\n✅ Todas as fotos estão OK!"))
