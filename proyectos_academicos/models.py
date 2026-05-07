from django.db import models
from django.contrib.auth.models import User
class Proyecto(models.Model):
    ESTADO_CHOICES = [
        ('enviado', 'Enviado'),
        ('revision', 'En Revision'),
        ('aprobado', 'Aprobado'),
    ]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    estudiante = models.ForeignKey(User, related_name='proyectos', on_delete=models.CASCADE)
    documento = models.FileField(upload_to='proyectos/')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='enviado')
    fecha_envio = models.DateTimeField(auto_now_add=True)
    fecha_revision = models.DateTimeField(null=True, blank=True)
    calificacion = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    def __str__(self):
        return self.titulo