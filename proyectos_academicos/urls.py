from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'proyectos_academicos'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('detalle/<int:pk>/', views.ProyectoDetailView.as_view(), name='detalle_proyecto'),
    path('comentario/<int:pk>/', views.agregar_comentario, name='agregar_comentario'),
]