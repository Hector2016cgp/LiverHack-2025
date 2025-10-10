# candidato/models.py
from django.db import models
from django.contrib.auth.models import User
from reclutamiento.models import Vacante

class Candidato(models.Model):
    """
    Información específica de un candidato que postula a vacantes.
    Se relaciona con User y puede almacenar CV, experiencia, y estado de postulaciones.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cv = models.FileField(upload_to='cvs/', null=True, blank=True)
    linkedin = models.URLField(max_length=200, null=True, blank=True)
    github = models.URLField(max_length=200, null=True, blank=True)
    resumen = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - Candidato'


class Postulacion(models.Model):
    """
    Relaciona un candidato con una vacante específica.
    Permite registrar el estado de su postulación y fecha.
    """
    ESTADO_CHOICES = [
        ('Recibida', 'Recibida'),
        ('En Revisión', 'En Revisión'),
        ('Entrevista', 'Entrevista'),
        ('Aceptada', 'Aceptada'),
        ('Rechazada', 'Rechazada'),
    ]

    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    vacante = models.ForeignKey(Vacante, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Recibida')
    fecha_postulacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('candidato', 'vacante')

    def __str__(self):
        return f'{self.candidato.user.username} -> {self.vacante.titulo}'
