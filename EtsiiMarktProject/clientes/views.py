from django.http import HttpResponse
from django.shortcuts import render
from .models import Cliente

# Listado de clientes (index)
def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/listado.html', {'clientes': clientes})