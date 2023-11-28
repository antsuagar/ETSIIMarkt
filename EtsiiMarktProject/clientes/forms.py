from django import forms
from django.contrib.auth.models import User
from .models import Cliente
from django.contrib.auth.password_validation import validate_password

class RegistroClienteForm(forms.ModelForm):
    clave = forms.CharField(widget=forms.PasswordInput)
    usuario = forms.CharField()

    class Meta:
        model = Cliente
        fields = ['usuario','clave','email','nombre','apellidos','direccion','telefono']
    
    def clean_clave(self):
        clave = self.cleaned_data.get('clave')
        validate_password(clave, self.instance)  # Realiza las validaciones de contraseña de Django
        return clave
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['usuario'].help_text = 'Obligatorio. Debe ser único'
        self.fields['clave'].help_text = 'Obligatorio'
        self.fields['email'].help_text = 'Obligatorio. Debe ser único, y no vale el de ejemplo'
