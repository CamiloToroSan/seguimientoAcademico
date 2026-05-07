from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'proyectos_academicos'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='proyectos_academicos:login'), name='logout'),
    path('', views.ProyectoListView.as_view(), name='lista_proyectos'),
    path('crear/', views.ProyectoCreateView.as_view(), name='crear_proyecto'),
    path('editar/<int:pk>/', views.ProyectoUpdateView.as_view(), name='editar_proyecto'),
    path('eliminar/<int:pk>/', views.ProyectoDeleteView.as_view(), name='eliminar_proyecto'),
    path('detalle/<int:pk>/', views.ProyectoDetailView.as_view(), name='detalle_proyecto'),
    path('comentario/<int:pk>/', views.agregar_comentario, name='agregar_comentario'),
    path('exportar/csv/', views.exportar_csv, name='exportar_csv'),
    path('docente/actualizar/<int:pk>/', views.docente_actualizar, name='docente_actualizar'),
]