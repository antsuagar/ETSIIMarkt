from django.http import HttpResponse
from django.shortcuts import render
from .models import Producto, Categoria

#Catalogo de Productos
def catalogo(request):
    productos = Producto.objects.all()
    return render(request, 'catalogo.html', {'productos': productos})

def catalogo(request):
    query = request.GET.get('q', '')
    query_filtro = request.GET.get('filtro', 'nombre')

    productos = Producto.objects.all()

    if query_filtro == 'nombre':
        productos = productos.filter(nombre__icontains=query)
    elif query_filtro == 'fabricante':
        productos = productos.filter(fabricante__nombre__icontains=query)
    elif query_filtro == 'categoria':
        productos = productos.filter(categoria__nombre__icontains=query)
    elif query_filtro == 'precio':
        if len(query)==0:
            productos = productos.filter(nombre__icontains=query)
        else: 
            productos = productos.filter(precio__lt=query)

    return render(request, 'catalogo.html', {'productos': productos, 'query': query, 'query_filtro': query_filtro})