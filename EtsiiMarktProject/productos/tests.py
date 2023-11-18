from django.test import TestCase
from .models import Categoria, Fabricante, Producto

class ProductoTestCase(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre='Electrodomestico')
        self.fabricante = Fabricante.objects.create(nombre='Fabricante')
        self.producto = Producto.objects.create(
            categoria=self.categoria,
            fabricante=self.fabricante,
            nombre='Producto de prueba',
            precio=100.0,
            descripcion='Descripción de prueba',
            cantidad=10,
        )

    def test_producto_agotado(self):
        self.producto.cantidad = 0
        self.assertTrue(self.producto.producto_agotado)

    def test_get_productos_by_categoria(self):
        productos_categoria = Producto.get_productos_by_categoria(self.categoria)
        self.assertIn(self.producto, productos_categoria)

    def test_get_productos_by_fabricante(self):
        productos_fabricante = Producto.get_productos_by_fabricante(self.fabricante)
        self.assertIn(self.producto, productos_fabricante)

    def test_get_productos_by_precio(self):
        productos_precio = Producto.get_productos_by_precio(50.0, 150.0)
        self.assertIn(self.producto, productos_precio)
