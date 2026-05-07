# Asegúrate de tener estos imports (si no, agrégalos)
from django.views.generic import DetailView
from django.core.mail import send_mail
from django.conf import settings
from .models import Comentario, Proyecto
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin


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
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Proyecto
from .forms import ProyectoForm


class ProyectoCreateView(LoginRequiredMixin, CreateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyectos/form.html'
    success_url = reverse_lazy('proyecto_list')
    def form_valid(self, form):
        form.instance.estudiante = self.request.user
        return super().form_valid(form)
    

class ProyectoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyectos/form.html'
    success_url = reverse_lazy('proyecto_list')
    def test_func(self):
        return self.get_object().estudiante == self.request.user
    
    
class ProyectoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Proyecto
    template_name = 'proyectos/confirmar_delete.html'
    success_url = reverse_lazy('proyecto_list')
    def test_func(self):
        return self.get_object().estudiante == self.request.user
     
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
