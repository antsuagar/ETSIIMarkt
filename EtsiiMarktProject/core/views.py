from django.http import HttpResponse
from django.shortcuts import render
from productos.models import Producto, Categoria

def index(request):    
    user = request.user
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'home.html', {'user': user, 'productos': productos, 'categorias': categorias})
    