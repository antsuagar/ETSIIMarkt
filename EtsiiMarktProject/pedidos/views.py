import uuid
from django.shortcuts import get_object_or_404, render

from .models import Pedido, ProductoPedido
from productos.models import Fabricante, Producto, Categoria

# Create your views here.
def carrito(request):

    if request.user.is_authenticated:
        user=request.user
        pedido, created = Pedido.objects.get_or_create(user=user)
        items = pedido.get_productos_carrito() 
    else:
        if 'anonimo_id' not in request.session:
            request.session['anonimo_id'] = str(uuid.uuid4())
            anonimo_id = request.session['anonimo_id']
            nuevo_pedido = Pedido(user=None,id_transaccion=anonimo_id)
            nuevo_pedido.save()
            items = []
            pedido = {'get_total_carrito':0, 'get_productos_carrito':0}
                
               
        else:
            anonimo_id = request.session['anonimo_id']
            pedido = get_object_or_404(Pedido, id_transaccion=anonimo_id)
            items = pedido.get_productos_carrito()
            
          
        

    context={'items': items, 'pedido': pedido}
    return render(request, 'productos/carrito.html', context)

def actualizar(request, producto_id):
    q_cantidad = request.POST.get('cantidad', '1')
    q_producto = get_object_or_404(Producto, pk=producto_id)

    if request.user.is_authenticated:
        user=request.user
        pedido, created = Pedido.objects.get_or_create(user=user)
      
    else:
        anonimo_id = request.session['anonimo_id']
        pedido = get_object_or_404(Pedido, id_transaccion=anonimo_id)
        
        
            
    producto_pedido, createdP= ProductoPedido.objects.get_or_create(pedido=pedido,producto=q_producto)
    producto_pedido.cantidad = q_cantidad
    producto_pedido.save()   

    items = pedido.get_productos_carrito()

    context={'items': items, 'pedido': pedido}
    return render(request, 'productos/carrito.html', context)



    

def eliminar(request, producto_id):
    q_producto = get_object_or_404(Producto, pk=producto_id)

    if request.user.is_authenticated:
        user=request.user
        pedido, created = Pedido.objects.get_or_create(user=user)
      
    else:
        anonimo_id = request.session['anonimo_id']
        pedido = get_object_or_404(Pedido, id_transaccion=anonimo_id)
        
        
            
    producto_pedido, createdP= ProductoPedido.objects.get_or_create(pedido=pedido,producto=q_producto)
    producto_pedido.delete()   

    items = pedido.get_productos_carrito()

    context={'items': items, 'pedido': pedido}
    return render(request, 'productos/carrito.html', context)