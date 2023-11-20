from django.http import HttpResponse
from django.shortcuts import render
<<<<<<< HEAD
from .models import Producto

#Catalogo de Productos
def catalogo(request):
    productos = Producto.objects.all()
    return render(request, 'catalogo.html', {'productos': productos})
<<<<<<< HEAD
=======


def index(request):
    contexto = {'productos':'Incluir listado de productos'}
    
    return render(request, 'productos.html', contexto)
>>>>>>> a316c19f ([dev] Vista base y de productos)
=======

>>>>>>> 7a6efd02d3ba70b9476f1f03c7959ec1114785d6
