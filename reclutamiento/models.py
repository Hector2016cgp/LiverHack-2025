from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Vacante(models.Model):
    ESTADO_CHOICES = [
        ('Abierta', 'Abierta'),
        ('En Proceso', 'En Proceso'),
        ('Cerrada', 'Cerrada'),
    ]

    TIPO_CONTRATO_CHOICES = [
        ('Tiempo Completo', 'Tiempo Completo'),
        ('Medio Tiempo', 'Medio Tiempo'),
        ('Por Proyecto', 'Por Proyecto'),
        ('Remoto', 'Remoto'),
    ]
    
    PRIORIDAD_CHOICES = [
        ('Baja', 'Baja'),
        ('Media', 'Media'),
        ('Alta', 'Alta'),
    ]

    AREA_CHOICES = [
        ('Tecnología E Informática', 'Tecnología E Informática'),
        ('Producto Digital', 'Producto Digital'),
        ('Artes Y Diseño', 'Artes Y Diseño'),
        ('Finanzas, Control De Gestión', 'Finanzas, Control De Gestión'),
        ('Data Y Business Intelligence', 'Data Y Business Intelligence'),
        ('Marketing', 'Marketing'),
        ('Logística, Compras Y Abastecimiento', 'Logística, Compras Y Abastecimiento'),
        ('Procesos, Estrategia Y Transformación', 'Procesos, Estrategia Y Transformación'),
        ('Legal', 'Legal'),
        ('Administración Y Secretariado', 'Administración Y Secretariado'),
        ('Sustentabilidad Y Medio Ambiente', 'Sustentabilidad Y Medio Ambiente'),
        ('Recursos Humanos', 'Recursos Humanos'),
        ('Comunicación y Periodismo', 'Comunicación y Periodismo'),
        ('Prevención De Riesgos', 'Prevención De Riesgos'),
        ('Producción Y Manufactura', 'Producción Y Manufactura'),
        ('Inmobiliaria', 'Inmobiliaria'),
    ]

    titulo = models.CharField(max_length=200, verbose_name="Título del Puesto")
    departamento = models.CharField(max_length=50, choices=AREA_CHOICES)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='Abierta')
    ubicacion = models.CharField(max_length=100)
    nivel = models.CharField(max_length=50)
    tipo_contrato = models.CharField(max_length=50, choices=TIPO_CONTRATO_CHOICES, default='Tiempo Completo')
    prioridad = models.CharField(max_length=50, choices=PRIORIDAD_CHOICES, default='Media')
    salario_minimo = models.IntegerField(null=True, blank=True)
    salario_maximo = models.IntegerField(null=True, blank=True)
    fecha_cierre = models.DateField()
    responsable_rh = models.CharField(max_length=100, verbose_name="Responsable RH")
    descripcion = models.TextField(verbose_name="Descripción del Puesto")
    requisitos = models.TextField()

    def __str__(self):
        return self.titulo


class Profile(models.Model):
    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
        ('P', 'Prefiero no decirlo')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True, null=True, help_text='Opcional.')
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True, help_text='Opcional.')

    def __str__(self):
        return f'Perfil de {self.user.username}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Guardar el perfil solo si existe
    if hasattr(instance, 'profile'):
        instance.profile.save()
