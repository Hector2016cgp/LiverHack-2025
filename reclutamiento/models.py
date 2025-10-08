from django.db import models
from django.utils import timezone

# Create your models here.

class Vacante(models.Model):
    
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

    # Campos del formulario
    titulo = models.CharField(max_length=200, verbose_name="Título del Puesto")
    departamento = models.CharField(max_length=50, choices=AREA_CHOICES)
    ubicacion = models.CharField(max_length=100)
    nivel = models.CharField(max_length=50) # Mejor si tuviera choices como "Junior", "Senior", etc.
    tipo_contrato = models.CharField(max_length=50, choices=TIPO_CONTRATO_CHOICES, default='Tiempo Completo')
    prioridad = models.CharField(max_length=50, choices=PRIORIDAD_CHOICES, default='Media')
    salario_minimo = models.IntegerField(null=True, blank=True)
    salario_maximo = models.IntegerField(null=True, blank=True)
    # fecha_publicacion = models.DateField()
    fecha_cierre = models.DateField()
    responsable_rh = models.CharField(max_length=100, verbose_name="Responsable RH")
    descripcion = models.TextField(verbose_name="Descripción del Puesto")
    requisitos = models.TextField()

    def __str__(self):
        return self.titulo