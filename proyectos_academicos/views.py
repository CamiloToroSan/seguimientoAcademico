import csv
from django.http import HttpResponse
from django.utils import timezone

class ProyectoListView(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = 'proyectos_academicos/proyecto_list.html'
    context_object_name = 'proyectos'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.groups.filter(name='Docente').exists():
            qs = qs.filter(estudiante=self.request.user)
        estado = self.request.GET.get('estado')
        estudiante_id = self.request.GET.get('estudiante')
        if estado:
            qs = qs.filter(estado=estado)
        if estudiante_id and self.request.user.groups.filter(name='Docente').exists():
            qs = qs.filter(estudiante__id=estudiante_id)
        return qs.order_by('-fecha_envio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estado_choices'] = Proyecto.ESTADO_CHOICES
        if self.request.user.groups.filter(name='Docente').exists():
            from django.contrib.auth.models import User
            context['estudiantes'] = User.objects.filter(groups__name='Estudiante')
        context['filtro_estado'] = self.request.GET.get('estado', '')
        context['filtro_estudiante'] = self.request.GET.get('estudiante', '')
        return context


def exportar_csv(request):
    if not request.user.groups.filter(name='Docente').exists():
        return redirect('proyectos_academicos:lista_proyectos')
    proyectos = Proyecto.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="proyectos.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Título', 'Estudiante', 'Estado', 'Fecha envío', 'Calificación'])
    for p in proyectos:
        writer.writerow([p.id, p.titulo, p.estudiante.username, p.estado, p.fecha_envio, p.calificacion])
    return response

@login_required
def docente_actualizar(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if not request.user.groups.filter(name='Docente').exists():
        return redirect('proyectos_academicos:lista_proyectos')
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        calificacion = request.POST.get('calificacion')
        if nuevo_estado in dict(Proyecto.ESTADO_CHOICES):
            proyecto.estado = nuevo_estado
            proyecto.fecha_revision = timezone.now()
        if calificacion:
            proyecto.calificacion = calificacion
        proyecto.save()
        if nuevo_estado == 'aprobado':
            send_mail(
                subject='Tu proyecto ha sido aprobado',
                message=f'Felicidades, tu proyecto "{proyecto.titulo}" ha sido aprobado.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[proyecto.estudiante.email],
                fail_silently=False,
            )
        return redirect('proyectos_academicos:lista_proyectos')
    return render(request, 'proyectos_academicos/docente_form.html', {'proyecto': proyecto})

