import uuid
from django.shortcuts import get_object_or_404, render, redirect

from .models import DireccionEnvio, Pedido, ProductoPedido, EstadoProducto
from django.contrib import messages
from productos.models import Producto
from datetime import datetime 
from django.core.mail import send_mail
from smtplib import SMTPRecipientsRefused
from django.db.models import Q


# Create your views here.
def carrito(request):

    if request.user.is_authenticated:
        user=request.user
        pedido, created = Pedido.objects.get_or_create(user=user)
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

    items = pedido.get_lista_de_productos_carrito()

    context={'items': items, 'pedido': pedido}
    return render(request, 'productos/carrito.html', context)


def formulario_envio(request):

    return render(request, 'envios/formulario_envio.html')

def procesar_pedido(request):
    
    email = request.POST.get('email')
    direccion = request.POST.get('direccion')
    ciudad = request.POST.get('ciudad')
    codigo_postal = request.POST.get('postal')
    id_transaccion = request.POST.get('id_transaccion')
    
    emails = [email]


    fecha_pedido = datetime.now()

    if request.user.is_authenticated:
        user=request.user
        pedido = get_object_or_404(Pedido, user=user)
      
    else:
        anonimo_id = request.session['anonimo_id']
        pedido = get_object_or_404(Pedido, id_transaccion=anonimo_id)
        user = None
        del request.session['anonimo_id']

    
    id_pedido = pedido.id 
    nombre_productos = [p.producto.nombre for p in pedido.get_lista_de_productos_carrito()]
    total = pedido.get_total_carrito
    factura = ', '.join(nombre_productos)

    try:
        send_mail(
        "Su pedido en Etsii Markt esta en marcha",
        "Gracias por comprar con nosotros, le informamos que su pedido de {0} con un total de {1} esta en marcha y se enviará a la dirección proporcionada: {2} en {3}, {4}. Podra rastrear su pedido con el siguiente enlace /seguimiento/{5}".format(factura, total, direccion, ciudad, codigo_postal, id_pedido),
        "etsiiMarktProyect@outlook.es",
        emails,
        fail_silently=False,
        )
    except SMTPRecipientsRefused as e:
        messages.error('Error, la dirección de correo introducida: {0} es invalida'.format(email))
        return render(request, 'envios/formulario_envio.html') 

    direccion_pedido, created = DireccionEnvio.objects.get_or_create(user=user, pedido=pedido, direccion=direccion, ciudad=ciudad, codigo_postal=codigo_postal)
    pedido.fecha_pedido = fecha_pedido
    pedido.completado = True
    pedido.id_transaccion = id_transaccion
    pedido.estado = EstadoProducto.EN_PREPARACION

    direccion_pedido.save()
    pedido.save()


    messages.success(request, 'El pedido se ha completado correctamente, se ha enviado un correo con el seguimiento y puede acceder a el con el siguiente enlace: .../seguimiento/{0}'.format(id_pedido))
    
 
    return render(request, 'home.html')

def pedidos_usuario(request):

    if request.user.is_authenticated:
        user=request.user
      
    else:
        messages.error('Ups, registrese para ver el seguimiento de sus pedidos')
        return render(request, 'envios/seguimiento.html')
    
    pedidos = Pedido.objects.all().filter(Q(user=user) & Q(completado=True))

    return render(request, 'envios/seguimiento.html', {'pedidos': pedidos})

