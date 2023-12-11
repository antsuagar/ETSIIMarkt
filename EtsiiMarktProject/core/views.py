import random
import uuid
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from pedidos.models import Pedido
from productos.models import Producto, Categoria


def index(request):    
    items = list(Producto.objects.all())
    productos = Producto.objects.all().order_by('?')[:4]
    categorias = Categoria.objects.all()
    return render(request, 'home.html', {'productos': productos, 'categorias': categorias})

def header(request):
    user = request.user
    
    #Copiado y pegado del carrito. Sirve para que se muestre el número de productos en la cesta
    if request.user.is_authenticated:
        user=request.user
        pedido, created = Pedido.objects.get_or_create(user=user,completado=False)
        items = pedido.get_lista_de_productos_carrito() 
    else:
        if 'anonimo_id' not in request.session:
            request.session['anonimo_id'] = str(uuid.uuid4())
            anonimo_id = request.session['anonimo_id']
            nuevo_pedido, created = Pedido.objects.get_or_create(user=None,id_transaccion=anonimo_id)
            nuevo_pedido.save()
            items = []
            pedido = {'get_total_carrito':0, 'get_productos_carrito':0}
       
        else:
            anonimo_id = request.session['anonimo_id']
            pedido = get_object_or_404(Pedido, id_transaccion=anonimo_id)
            items = pedido.get_lista_de_productos_carrito()

    numero_carrito = len(items)
    return render(request, 'header.html', {'user': user, 'numero_carrito': numero_carrito})

def nosotros(request):  
    return render(request, 'empresa/nosotros.html')

def devoluciones(request):  
    return render(request, 'empresa/devoluciones.html')
