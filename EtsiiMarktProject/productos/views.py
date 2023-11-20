from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    contexto = {'productos':'Incluir listado de productos'}
    
    return render(request, 'productos.html', contexto)