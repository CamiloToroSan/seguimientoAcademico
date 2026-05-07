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