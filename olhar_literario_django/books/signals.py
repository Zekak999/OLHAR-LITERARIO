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
    """
    if created:
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
