urlpatterns += [
    path('exportar/csv/', views.exportar_csv, name='exportar_csv'),
    path('docente/actualizar/<int:pk>/', views.docente_actualizar, name='docente_actualizar'),
]