from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
import csv

from .models import Proyecto, Comentario
from .forms import ProyectoForm

# ==================== MIXINS DE PERMISOS ====================
class EstudianteRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Estudiante').exists()
    def handle_no_permission(self):
        return redirect('proyectos_academicos:lista_proyectos')

class DocenteRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Docente').exists()
    def handle_no_permission(self):
        return redirect('proyectos_academicos:lista_proyectos')

class EsPropietarioMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.estudiante
    def handle_no_permission(self):
        return redirect('proyectos_academicos:lista_proyectos')

# ==================== VISTAS CRUD ====================

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

class ProyectoCreateView(LoginRequiredMixin, EstudianteRequiredMixin, CreateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyectos_academicos/proyecto_form.html'
    success_url = reverse_lazy('proyectos_academicos:lista_proyectos')

    def form_valid(self, form):
        form.instance.estudiante = self.request.user
        return super().form_valid(form)

class ProyectoUpdateView(LoginRequiredMixin, EsPropietarioMixin, UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyectos_academicos/proyecto_form.html'
    success_url = reverse_lazy('proyectos_academicos:lista_proyectos')

    def dispatch(self, request, *args, **kwargs):
        proyecto = self.get_object()
        if proyecto.estado == 'aprobado':
            return redirect('proyectos_academicos:lista_proyectos')
        return super().dispatch(request, *args, **kwargs)

class ProyectoDeleteView(LoginRequiredMixin, EsPropietarioMixin, DeleteView):
    model = Proyecto
    template_name = 'proyectos_academicos/proyecto_confirm_delete.html'
    success_url = reverse_lazy('proyectos_academicos:lista_proyectos')

    def dispatch(self, request, *args, **kwargs):
        proyecto = self.get_object()
        if proyecto.estado == 'aprobado':
            return redirect('proyectos_academicos:lista_proyectos')
        return super().dispatch(request, *args, **kwargs)

# ==================== VISTA DE DETALLE Y COMENTARIOS ====================

class ProyectoDetailView(LoginRequiredMixin, DetailView):
    model = Proyecto
    template_name = 'proyectos_academicos/proyecto_detail.html'
    context_object_name = 'proyecto'

@login_required
def agregar_comentario(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if proyecto.estado == 'aprobado':
        return redirect('proyectos_academicos:detalle_proyecto', pk=pk)
    if request.method == 'POST':
        texto = request.POST.get('texto')
        if texto:
            Comentario.objects.create(proyecto=proyecto, usuario=request.user, texto=texto)
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

# ==================== EXPORTACIÓN CSV ====================

@login_required
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

# ==================== VISTA DE ACTUALIZACIÓN POR DOCENTE ====================

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