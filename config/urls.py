from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from proyectos_academicos.views import (
    ProyectoListView, 
    ProyectoCreateView, 
    ProyectoUpdateView, 
    ProyectoDeleteView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('proyectos_academicos/', include('proyectos_academicos.urls')),
    path('', auth_views.LoginView.as_view(template_name='proyectos/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('proyectos/', ProyectoListView.as_view(), name='proyecto_list'),
    path('proyectos/nuevo/', ProyectoCreateView.as_view(), name='proyecto_create'),
    path('proyectos/editar/<int:pk>/', ProyectoUpdateView.as_view(), name='proyecto_update'),
    path('proyectos/eliminar/<int:pk>/', ProyectoDeleteView.as_view(), name='proyecto_delete'),
]
