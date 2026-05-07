from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from .models import Proyecto

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['titulo', 'descripcion', 'documento']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('titulo', css_class='form-control'),
            Field('descripcion', css_class='form-control', rows=4),
            Field('documento', css_class='form-control'),
            Submit('submit', 'Guardar', css_class='btn btn-success mt-3')
        )