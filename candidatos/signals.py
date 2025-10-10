from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Candidato

@receiver(post_save, sender=User)
def create_candidato_for_user(sender, instance, created, **kwargs):
    """
    Crea automáticamente un objeto Candidato cuando se crea un nuevo usuario
    que no es staff/superuser.
    """
    if created and not (instance.is_staff or instance.is_superuser):
        Candidato.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_candidato(sender, instance, **kwargs):
    """
    Guarda el objeto Candidato cuando se guarda el usuario.
    """
    if hasattr(instance, 'candidato'):
        instance.candidato.save()