from django.contrib import admin
from .models import Proyecto

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'estudiante', 'estado', 'calificacion', 'fecha_envio']
    list_filter = ['estado', 'fecha_envio']
    search_fields = ['titulo', 'estudiante__username']
    readonly_fields = ['fecha_envio']