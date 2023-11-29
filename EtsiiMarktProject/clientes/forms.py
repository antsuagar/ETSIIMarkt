from django import forms
from django.contrib.auth.models import User
from .models import Cliente
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
import pdb

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


class UserOrEmailAuthenticationForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario o correo electrónico')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

    def clean(self):
        cleaned_data = super().clean()
        username_email = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username_email and password:
            # Intenta autenticar con el nombre de usuario
            user_by_username = authenticate(username=username_email, password=password)

            # Intenta autenticar con el correo electrónico
            username_email = obtener_username_por_correo_cliente(username_email)
            user_by_email = authenticate(username=username_email, password=password)

            if user_by_username is None and user_by_email is None:
                raise forms.ValidationError('Nombre de usuario o correo electrónico incorrecto')

            # Establece el usuario autenticado en cleaned_data
            if user_by_username:
                cleaned_data['user'] = user_by_username
            elif user_by_email:
                cleaned_data['username'] = user_by_email
                cleaned_data['user'] = user_by_email

        return cleaned_data

def obtener_username_por_correo_cliente(correo_cliente):
    try:
        cliente = Cliente.objects.get(email=correo_cliente)
        return cliente.user.username if cliente.user else None
    except Cliente.DoesNotExist:
        return None