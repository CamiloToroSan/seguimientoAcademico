from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Comentario(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.proyecto.titulo}"
    
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
