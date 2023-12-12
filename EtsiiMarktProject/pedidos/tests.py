from django.test import TestCase
from django.contrib.auth.models import User
from .models import Pedido, Producto, ProductoPedido, DireccionEnvio, Reclamacion, EstadoProducto

class PedidoModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.pedido = Pedido.objects.create(
            user=self.user,
            destinatario='John Doe',
            completado=False,
            id_transaccion='ABC123',
            estado=EstadoProducto.EN_PREPARACION
        )
        
    def test_pedido_creado_correctamente(self):
        pedido = Pedido.objects.get(id=self.pedido.id)
        self.assertEqual(pedido.destinatario, 'John Doe')
        self.assertFalse(pedido.completado)
        self.assertEqual(pedido.id_transaccion, 'ABC123')
        self.assertEqual(pedido.get_estado(), 'En preparación')

    def test_get_total_carrito(self):
        producto = Producto.objects.create(nombre='Producto de prueba', precio=50)
        ProductoPedido.objects.create(producto=producto, pedido=self.pedido, cantidad=3)
        
        # Realizar pruebas relacionadas con el cálculo del total del carrito aquí
        
    # Puedes continuar con pruebas para otros métodos y propiedades de los modelos

class DireccionEnvioModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.pedido = Pedido.objects.create(user=self.user, completado=False)
        self.direccion_envio = DireccionEnvio.objects.create(
            user=self.user,
            pedido=self.pedido,
            direccion='Calle Principal 123',
            ciudad='Ciudad Test',
            codigo_postal='12345'
        )
        
    def test_direccion_envio_creada_correctamente(self):
        direccion_envio = DireccionEnvio.objects.get(id=self.direccion_envio.id)
        self.assertEqual(direccion_envio.direccion, 'Calle Principal 123')
        self.assertEqual(direccion_envio.ciudad, 'Ciudad Test')
        self.assertEqual(direccion_envio.codigo_postal, '12345')

    # Continuar con más pruebas para este modelo y sus funcionalidades
    
# Puedes añadir pruebas similares para los otros modelos como ProductoPedido y Reclamacion

