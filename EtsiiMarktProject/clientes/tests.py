from django.test import TestCase
from django.contrib.auth.models import User
from .models import DireccionCliente

class DireccionClienteTest(TestCase):
    
    def setUp(self):
        # Crear un usuario para las pruebas
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        # Crear una dirección de prueba
        self.direccion_cliente = DireccionCliente.objects.create(
            user=self.user,
            direccion='Calle Principal 123',
            ciudad='Ciudad Test',
            postal='12345',
            formaPago='contrarrempolso'
        )

    def test_direccion_cliente_creada_correctamente(self):
        direccion = DireccionCliente.objects.get(id=self.direccion_cliente.id)
        self.assertEqual(direccion.user.username, 'testuser')
        self.assertEqual(direccion.direccion, 'Calle Principal 123')
        self.assertEqual(direccion.ciudad, 'Ciudad Test')
        self.assertEqual(direccion.postal, '12345')
        self.assertEqual(direccion.formaPago, 'contrarrempolso')

    def test_str_method(self):
        direccion = DireccionCliente.objects.get(id=self.direccion_cliente.id)
        self.assertEqual(str(direccion), f"Dirección de {direccion.user}")

    def test_default_formaPago(self):
        direccion = DireccionCliente.objects.create(
            user=self.user,
            direccion='Otra Calle 456',
            ciudad='Otra Ciudad',
            postal='54321'
        )
        self.assertEqual(direccion.formaPago, 'contrarrempolso')
