from django.http import HttpResponse
from django.shortcuts import render
from productos.models import Producto

def index(request):    
    user = request.user
    productos = Producto.objects.all()
    return render(request, 'home.html', {'user': user, 'productos': productos})

def nosotros(request):  
    return render(request, 'empresa/nosotros.html')

def devoluciones(request):  
    return render(request, 'empresa/devoluciones.html')
