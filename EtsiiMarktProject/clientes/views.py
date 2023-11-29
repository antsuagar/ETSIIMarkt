from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from .forms import UserOrEmailAuthenticationForm
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm

def index(request):    
    user = request.user
    return render(request, '/home.html', {'user': user})

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