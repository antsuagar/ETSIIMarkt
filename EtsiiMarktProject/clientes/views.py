from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .models import Cliente
from .forms import RegistroClienteForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from .forms import UserOrEmailAuthenticationForm
from django.views.generic.edit import FormView

class RegistroClienteView(CreateView):
    model = Cliente
    form_class = RegistroClienteForm
    template_name = 'clientes/registro_cliente.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        # Aquí es donde se maneja la creación del User y la asociación con el Cliente
        # Extraer información del formulario
        username = form.cleaned_data['usuario']
        nombre = form.cleaned_data['nombre']
        apellidos = form.cleaned_data['apellidos']
        password = form.cleaned_data['clave']
        email = form.cleaned_data['email']        
        direccion = form.cleaned_data['direccion']
        telefono = form.cleaned_data['telefono']

        # Crear el User solo con nombre y contraseña
        user = User.objects.create_user(username=username, password=password)
        if nombre:
            user.first_name = nombre
        if apellidos:
            user.last_name = apellidos
        user.email = email
        user.save()

        # Crear el Cliente asociado al User
        cliente = form.save(commit=False)
        cliente.user = user        
        if not nombre:
            nombre = email
        cliente.nombre = nombre

        if apellidos:
            cliente.apellidos = apellidos        
        if direccion:
            cliente.direccion = direccion
        if telefono:
            cliente.telefono = telefono
        cliente.email = email
        cliente.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        # Manejar el caso en que el formulario no sea válido
        return self.render_to_response(self.get_context_data(form=form))


class IniciarSesionView(FormView):
    template_name = 'clientes/login.html'
    form_class = UserOrEmailAuthenticationForm
    success_url = 'index'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        # Intenta autenticar solo con el nombre de usuario
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            return redirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))