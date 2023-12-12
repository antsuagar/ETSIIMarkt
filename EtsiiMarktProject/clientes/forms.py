from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
import pdb
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from clientes.models import DireccionCliente

from pedidos.models import DireccionEnvio

class CustomUserCreationForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
	def clean_email(self):
		email = self.cleaned_data['email']

		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('Este correo electrónico ya está registrado')
		return email

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
        cliente = User.objects.get(email=correo_cliente)
        return cliente.username if cliente else None
    except User.DoesNotExist:
        return None
    
class CustomUserChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = User  
        fields = ['first_name', 'last_name', 'email']  

class UserDireccionForm(forms.ModelForm):
    class Meta:
        model = DireccionCliente
        fields = ['direccion', 'ciudad', 'postal', 'formaPago']