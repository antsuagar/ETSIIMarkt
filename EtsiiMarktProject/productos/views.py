import uuid
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404

from pedidos.models import Pedido, ProductoPedido

from productos.models import Fabricante, Producto, Categoria
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
    q_precioMin = request.GET.get('precioMin', '')
    q_precioMax = request.GET.get('precioMax', '')

    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    fabricantes = Fabricante.objects.all()

    if q_fabricante=='Fabricante':
        q_fabricante=''
    if q_categoria=='Electrodomestico':
        q_categoria=''
    if q_precioMin=='':
        q_precioMin=0
    if q_precioMax=='':
        q_precioMax=1000000000000

    productos = productos.filter( Q(fabricante__nombre__icontains=q_fabricante) & Q(categoria__nombre__icontains=q_categoria) & Q(precio__lte=q_precioMax) & Q(precio__gte=q_precioMin))
        

    return render(request, 'productos/catalogo.html', {'productos': productos, 'categorias': categorias,'fabricantes': fabricantes})

def detalle(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    cantidadPedida = request.GET.get('cantidad','')
    

    if cantidadPedida =='':
        return render(request, 'productos/detalle.html', {'producto': producto})

    elif request.user.is_authenticated:
        user=request.user
        nuevo_pedido, created = Pedido.objects.get_or_create(user=user)
        incluir_producto, createdP= ProductoPedido.objects.get_or_create(pedido=nuevo_pedido,producto=producto)
        incluir_producto.cantidad = incluir_producto.cantidad+int(cantidadPedida)
        nuevo_pedido.save()
        incluir_producto.save()     

    else:  
        if 'anonimo_id' not in request.session:
            request.session['anonimo_id'] = str(uuid.uuid4())
            anonimo_id = request.session['anonimo_id']
            nuevo_pedido = Pedido(user=None,id_transaccion=anonimo_id)
            nuevo_pedido.save()
            incluir_producto= ProductoPedido(pedido=nuevo_pedido, producto=producto, cantidad=int(cantidadPedida))
            incluir_producto.save()
                
               
        else:
            anonimo_id = request.session['anonimo_id']
            cesta = get_object_or_404(Pedido, id_transaccion=anonimo_id)
            incluir_producto, createdP= ProductoPedido.objects.get_or_create(pedido=cesta,producto=producto)
            incluir_producto.cantidad = incluir_producto.cantidad+int(cantidadPedida)
            incluir_producto.save() 
           

    messages.success(request, 'El producto se ha añadido al carrito de compra')
    return render(request, 'productos/detalle.html', {'producto': producto})

    
                            
