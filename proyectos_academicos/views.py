# Asegúrate de tener estos imports (si no, agrégalos)
from django.views.generic import DetailView
from django.core.mail import send_mail
from django.conf import settings
from .models import Comentario
from django.shortcuts import get_object_or_404, redirect


class ProyectoDetailView(LoginRequiredMixin, DetailView):
    model = Proyecto
    template_name = 'proyectos_academicos/proyecto_detail.html'
    context_object_name = 'proyecto'


def agregar_comentario(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    
    if proyecto.estado == 'aprobado':
        return redirect('proyectos_academicos:detalle_proyecto', pk=pk)
    
    if request.method == 'POST':
        texto = request.POST.get('texto')
        if texto:
            
            Comentario.objects.create(
                proyecto=proyecto,
                usuario=request.user,
                texto=texto
            )
            
            if request.user.groups.filter(name='Docente').exists():
                send_mail(
                    subject='Nuevo comentario en tu proyecto',
                    message=f'El docente ha comentado en tu proyecto "{proyecto.titulo}":\n\n{texto}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[proyecto.estudiante.email],
                    fail_silently=False,
                )
        return redirect('proyectos_academicos:detalle_proyecto', pk=pk)
    return redirect('proyectos_academicos:detalle_proyecto', pk=pk)