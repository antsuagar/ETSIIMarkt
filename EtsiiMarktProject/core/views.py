import random
import uuid
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from pedidos.models import Pedido
from productos.models import Producto, Categoria


def index(request):    
    user = request.user
    items = list(Producto.objects.all())
    productos = Producto.objects.all().order_by('?')[:4]
    categorias1 = Categoria.objects.all()
    categorias=categorias1.exclude(nombre='Todos los electrodomésticos')
    return render(request, 'home.html', {'productos': productos, 'categorias': categorias, 'user': user})

def nosotros(request):  
    return render(request, 'empresa/nosotros.html')

def devoluciones(request):  
    return render(request, 'empresa/devoluciones.html')

def custom_404(request, exception):
    return render(request, '404.html', status=404)
