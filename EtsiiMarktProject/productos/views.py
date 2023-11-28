from django.http import HttpResponse
from django.shortcuts import render
from .models import Fabricante, Producto, Categoria
from django.db.models import Q

#Catalogo de Productos
def catalogo(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    fabricantes = Fabricante.objects.all()

    
    return render(request, 'productos/catalogo.html', {'productos': productos, 'categorias': categorias, 'fabricantes': fabricantes})

def catalogo(request):
    query = request.GET.get('q', '')

    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    fabricantes = Fabricante.objects.all()


    productos = productos.filter(nombre__icontains=query)


    return render(request, 'productos/catalogo.html', {'productos': productos, 'categorias': categorias, 'fabricantes': fabricantes,   'query': query})

def catalogo2(request):
    q_fabricante = request.GET.get('fabricante', '')
    q_categoria = request.GET.get('categoria', '')
    q_precioMin = request.GET.get('precioMin', '0')
    q_precioMax = request.GET.get('precioMax', '1000')

    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    fabricantes = Fabricante.objects.all()

    if q_precioMax=='':
        q_precioMax=100000000000
    if q_precioMin=='':
        q_precioMin=0
    if q_fabricante=='Fabricante':
        q_fabricante=''
    if q_categoria=='Electrodomestico':
        q_categoria=''

    productos = productos.filter( Q(fabricante__nombre__icontains=q_fabricante) & Q(categoria__nombre__icontains=q_categoria) & Q(precio__lte=q_precioMax) & Q(precio__gte=q_precioMin))
        

    return render(request, 'productos/catalogo.html', {'productos': productos, 'categorias': categorias,'fabricantes': fabricantes})