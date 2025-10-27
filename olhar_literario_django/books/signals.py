"""
Signals para criar UserProfile automaticamente quando um User é criado
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile


@receiver(post_save, sender=User)
def criar_user_profile(sender, instance, created, **kwargs):
    """
    Cria automaticamente um UserProfile quando um novo User é criado.
    Isso evita erros ao tentar acessar user.profile quando não existe.
    
    Nota: Não cria durante o registro (raw=True) para evitar duplicação.
    O registro cria o profile com os dados completos.
    """
    # Pular se for um registro (a view cria o profile com dados)
    if created and not kwargs.get('raw', False):
        # Verificar se já existe profile (pode ter sido criado pela view)
        if not hasattr(instance, 'profile'):
            try:
                UserProfile.objects.get(user=instance)
            except UserProfile.DoesNotExist:
                UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def salvar_user_profile(sender, instance, **kwargs):
    """
    Salva o UserProfile quando o User é salvo.
    Garante que o profile sempre existe.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        # Se não tem profile, cria um
        UserProfile.objects.get_or_create(user=instance)
