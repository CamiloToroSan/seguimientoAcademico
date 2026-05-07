from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Proyecto
from .forms import ProyectoForm

class ProyectoListView(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = 'proyectos/lista.html'
    context_object_name = 'proyectos'


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