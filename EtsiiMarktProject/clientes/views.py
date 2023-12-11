from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from clientes.models import DireccionCliente
from productos.models import Producto

from pedidos.models import DireccionEnvio, Pedido, ProductoPedido
from .forms import CustomUserChangeForm, CustomUserCreationForm, UserDireccionForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from .forms import UserOrEmailAuthenticationForm
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def register(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()

            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            return redirect('/')
        else:
            data['form'] = user_creation_form

    return render(request, 'clientes/registro_cliente.html', data)

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
    
def perfil(request):
    user = request.user
    return render(request, 'clientes/perfil.html', {'user': user})

@login_required
def modificar_datos_usuario(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/perfil')  
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'clientes/modificar_perfil.html', {'form': form})

@login_required
def logout_personalizado(request):
    user=request.user
    pedido, created = Pedido.objects.get_or_create(user=user,completado=False)
    items = pedido.get_lista_de_productos_carrito() 
    if len(items) != 0:
        for item in items:
            producto, createdP= Producto.objects.get_or_create(nombre=item.producto.nombre)
            producto.cantidad = item.cantidad+producto.cantidad
            item.delete()  
            producto.save()
    return redirect('/logout')  

@login_required
def editar_direccion_envio(request):
    # Obtener la instancia de DireccionEnvio del usuario actual (asumiendo que tienes algún método para obtener al usuario actual)
    usuario_actual = request.user  # Obtener el usuario actual, puedes usar tu método de autenticación aquí

    # Buscar la dirección de envío del usuario actual o crear una nueva si no existe
    try:
        direccion_envio = DireccionCliente.objects.get(user=usuario_actual)  # Ajusta esto según tu modelo de cliente
    except DireccionCliente.DoesNotExist:
        direccion_envio = DireccionCliente(user=usuario_actual)
    
    if request.method == 'POST':
        form = UserDireccionForm(request.POST, instance=direccion_envio)
        if form.is_valid():
            form.save()
            return redirect('/perfil')  # Reemplaza 'ruta_de_redireccion' con la URL a donde quieres redirigir después de guardar la dirección
    else:
        form = UserDireccionForm(instance=direccion_envio)
    
    return render(request, 'clientes/direccion_envio.html', {'form': form, 'user': usuario_actual})