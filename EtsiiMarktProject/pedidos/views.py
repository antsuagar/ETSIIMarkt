import uuid
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
import stripe

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

    context={'items': items, 'pedido': pedido}
    return render(request, 'productos/carrito.html', context)

def actualizar(request, producto_id):
    q_cantidad = request.POST.get('cantidad', '1')
    q_producto = get_object_or_404(Producto, pk=producto_id)

    if request.user.is_authenticated:
        user=request.user
        pedido, created = Pedido.objects.get_or_create(user=user,completado=False)
      
    else:
        anonimo_id = request.session['anonimo_id']
        pedido = get_object_or_404(Pedido, id_transaccion=anonimo_id)

    producto_pedido, createdP= ProductoPedido.objects.get_or_create(pedido=pedido,producto=q_producto)
    q_producto.cantidad = q_producto.cantidad+(producto_pedido.cantidad-int(q_cantidad))
    producto_pedido.cantidad =q_cantidad
    producto_pedido.save() 
    q_producto.save()  

    

    items = pedido.get_lista_de_productos_carrito()

    context={'items': items, 'pedido': pedido}
    return render(request, 'productos/carrito.html', context)


def eliminar(request, producto_id):
    q_producto = get_object_or_404(Producto, pk=producto_id)

    if request.user.is_authenticated:
        user=request.user
        pedido, created = Pedido.objects.get_or_create(user=user,completado=False)
      
    else:
        anonimo_id = request.session['anonimo_id']
        pedido = get_object_or_404(Pedido, id_transaccion=anonimo_id)
        
        
            
    producto_pedido, createdP= ProductoPedido.objects.get_or_create(pedido=pedido,producto=q_producto)
    q_producto.cantidad = q_producto.cantidad+producto_pedido.cantidad
    producto_pedido.delete()  
    q_producto.save()  

    items = pedido.get_lista_de_productos_carrito()

    context={'items': items, 'pedido': pedido}
    return render(request, 'productos/carrito.html', context)


def formulario_envio(request, pedido_id):
    return render(request, 'envios/formulario_envio.html', {'pedido_id':pedido_id})

stripe.api_key = 'sk_test_51OJe72EuWRxRJueoRLXhuB2us5H5nJFQRn02WrVfTyGtZGVopiWMyfDJHk7y0mD7wVXnKPL5UXn7lkoIwjafoemJ0022EMLQvB'

def procesar_pedido(request):
    
    email = request.POST.get('email')
    direccion = request.POST.get('direccion')
    ciudad = request.POST.get('ciudad')
    codigo_postal = request.POST.get('postal')
    pedido_id = request.POST.get('pedido_id')
    forma_pago = request.POST.get('formaPago')
    pagado = request.POST.get('pagado','')
    pedido = get_object_or_404(Pedido,pk=pedido_id)

    if forma_pago=='pasarela' and pagado=='':
        return render(request, 'pedidos/payment.html', {'pedido':pedido, 'email':email, 'direccion': direccion, 'ciudad':ciudad, 'postal':codigo_postal,'formaPago':forma_pago}) 
    
    elif forma_pago=='pasarela' and pagado=='tarjeta':
        cantidad = request.POST.get('cantidad','0')
        amount = float(cantidad)*100
        token = request.POST.get('stripeToken')

        try:
            # Crear un cargo en Stripe
            cargo = stripe.Charge.create(
                amount=int(amount),
                currency='eur',  # Puedes cambiar a la moneda que prefieras
                description='pago etsiimarkt',
                source=token,
                
            )

            # Redirigir a la página de éxito si el pago se procesa correctamente
            #return redirect(reverse('exito'), amount=cargo.amount, currency=cargo.currency)
            url = reverse('exito', kwargs={'cantidad':cargo.amount})

        except stripe.error.CardError as e:
            # El pago ha sido rechazado por Stripe, redirigir a la página de error
            #error_msg = e.error.message
            #return redirect('error', error=error_msg)
            url = reverse('error', kwargs={'error':e.error.message})
            return HttpResponseRedirect(url)    
        
    emails = [email]


    fecha_pedido = datetime.now()

    if request.user.is_authenticated:
        user=request.user
      
    else:
        user = None
        del request.session['anonimo_id']

    
    id_pedido = pedido.id 
    nombre_productos = [p.producto.nombre for p in pedido.get_lista_de_productos_carrito()]
    total = pedido.get_total_carrito
    factura = ', '.join(nombre_productos)

    try:
        send_mail(
        "Su pedido en Etsii Markt esta en marcha",
        "Gracias por comprar con nosotros, le informamos que su pedido de {0} con un total de {1} esta en marcha y se enviará a la dirección proporcionada: {2} en {3}, {4}. Podra rastrear su pedido en nuestra página web introduciendo el número de su pedido: {5} en el apartado de pedidos realizados o estando registrado en nuestra web".format(factura, total, direccion, ciudad, codigo_postal, id_pedido),
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
    if forma_pago=='pasarela':
        pedido.id_transaccion = token
    else:
        pedido.id_transaccion = 'Contrareembolso'
    
    pedido.estado = EstadoProducto.EN_PREPARACION
    direccion_pedido.save()
    pedido.save()


    messages.success(request, 'Su pedido con id: {0}, se ha completado correctamente, se ha enviado un correo con el seguimiento y puede hacer su seguimiento en la pestañas Pedidos realizados'.format(id_pedido))
    
 
    return render(request, 'home.html')

def pedidos_usuario(request):
    
    if request.user.is_authenticated:
        user=request.user
        pedidos = Pedido.objects.all().filter(Q(user=user) & Q(completado=True))
      
    else:
        id_pedido= request.GET.get('idPedido','')
        if id_pedido=='':
            messages.success(request, 'Para poder hacer seguimiento de sus pedidos, registrese o indique número de su pedido')
            return render(request, 'envios/seguimiento.html')
        pedido = get_object_or_404(Pedido, id=id_pedido)
        pedidos =[pedido]
    
    return render(request, 'envios/seguimiento.html', {'pedidos': pedidos})



# Pasarela de pago


def procesar_pago(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        token = request.POST.get('stripeToken')
        cantidad = int(request.POST.get('cantidad','0'))

        try:
            # Crear un cargo en Stripe
            cargo = stripe.Charge.create(
                amount=cantidad*100,
                currency='eur',  # Puedes cambiar a la moneda que prefieras
                description='Pago de prueba',
                source=token,
            )

            # Redirigir a la página de éxito si el pago se procesa correctamente
            #return redirect(reverse('exito'), amount=cargo.amount, currency=cargo.currency)
            url = reverse('exito', kwargs={'cantidad':cargo.amount})
            return HttpResponseRedirect(url)

        except stripe.error.CardError as e:
            # El pago ha sido rechazado por Stripe, redirigir a la página de error
            #error_msg = e.error.message
            #return redirect('error', error=error_msg)
            url = reverse('error', kwargs={'error':e.error.message})
            return HttpResponseRedirect(url)            

    return render(request, 'pedidos/payment.html')

def exito(request, cantidad):
    context = {'cantidad': cantidad}
    return render(request, 'pedidos/payment_success.html', context)

def error(request, error):
    #error_msg = request.GET.get('error', 'Error en el pago')
    context = {'error': error}
    return render(request, 'pedidos/payment_failure.html', context)