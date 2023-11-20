from django.http import HttpResponse
from django.shortcuts import render
from .models import Producto

#Catalogo de Productos
def catalogo(request):
    productos = Producto.objects.all()
    return render(request, 'catalogo.html', {'productos': productos})

