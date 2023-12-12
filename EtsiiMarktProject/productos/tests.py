from django.test import TestCase
from .models import Categoria, Fabricante, Producto, Opinion
from django.contrib.auth.models import User

class CategoriaModelTest(TestCase):
    
    def test_str_method(self):
        categoria = Categoria.objects.create(nombre='Electrónica')
        self.assertEqual(str(categoria), 'Electrónica')

    def test_categoria_ordenamiento(self):
        Categoria.objects.create(nombre='B')
        Categoria.objects.create(nombre='C')
        Categoria.objects.create(nombre='A')
        categorias = Categoria.objects.all()
        self.assertEqual(categorias[0].nombre, 'A')
        self.assertEqual(categorias[1].nombre, 'B')
        self.assertEqual(categorias[2].nombre, 'C')
        
    # Puedes agregar más pruebas para otras funcionalidades del modelo Categoria
    
class FabricanteModelTest(TestCase):

    def test_str_method(self):
        fabricante = Fabricante.objects.create(nombre='Sony')
        self.assertEqual(str(fabricante), 'Sony')

    def test_fabricante_ordenamiento(self):
        Fabricante.objects.create(nombre='B')
        Fabricante.objects.create(nombre='C')
        Fabricante.objects.create(nombre='A')
        fabricantes = Fabricante.objects.all()
        self.assertEqual(fabricantes[0].nombre, 'A')
        self.assertEqual(fabricantes[1].nombre, 'B')
        self.assertEqual(fabricantes[2].nombre, 'C')

    # Puedes agregar más pruebas para otras funcionalidades del modelo Fabricante
    
class ProductoModelTest(TestCase):
    
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre='Electrónica')
        self.fabricante = Fabricante.objects.create(nombre='Sony')
        
    def test_producto_agotado(self):
        producto = Producto.objects.create(
            categoria=self.categoria,
            fabricante=self.fabricante,
            nombre='Televisor',
            precio=500,
            cantidad=0
        )
        self.assertTrue(producto.producto_agotado)

    def test_str_method(self):
        producto = Producto.objects.create(
            categoria=self.categoria,
            fabricante=self.fabricante,
            nombre='Televisor',
            precio=500,
            cantidad=10
        )
        self.assertEqual(str(producto), 'Televisor')

    def test_venta(self):
        producto = Producto.objects.create(
            categoria=self.categoria,
            fabricante=self.fabricante,
            nombre='Televisor',
            precio=500,
            cantidad=10
        )
        cantidad_vendida = 5
        self.assertEqual(producto.venta(cantidad_vendida), 5)

    def test_get_productos_by_categoria(self):
        producto_1 = Producto.objects.create(
            categoria=self.categoria,
            fabricante=self.fabricante,
            nombre='Televisor',
            precio=500,
            cantidad=10
        )
        producto_2 = Producto.objects.create(
            categoria=self.categoria,
            fabricante=self.fabricante,
            nombre='Computadora',
            precio=1000,
            cantidad=5
        )
        productos_categoria = Producto.get_productos_by_categoria(self.categoria)
        self.assertIn(producto_1, productos_categoria)
        self.assertIn(producto_2, productos_categoria)

    def test_get_productos_by_fabricante(self):
        fabricante_2 = Fabricante.objects.create(nombre='Samsung')
        producto_1 = Producto.objects.create(
            categoria=self.categoria,
            fabricante=self.fabricante,
            nombre='Televisor',
            precio=500,
            cantidad=10
        )
        producto_2 = Producto.objects.create(
            categoria=self.categoria,
            fabricante=fabricante_2,
            nombre='Teléfono',
            precio=800,
            cantidad=3
        )
        productos_fabricante = Producto.get_productos_by_fabricante(self.fabricante)
        self.assertIn(producto_1, productos_fabricante)
        self.assertNotIn(producto_2, productos_fabricante)

    def test_get_productos_by_precio(self):
        producto_1 = Producto.objects.create(
            categoria=self.categoria,
            fabricante=self.fabricante,
            nombre='Televisor',
            precio=500,
            cantidad=10
        )
        producto_2 = Producto.objects.create(
            categoria=self.categoria,
            fabricante=self.fabricante,
            nombre='Computadora',
            precio=1000,
            cantidad=5
        )
        productos_rango_precio = Producto.get_productos_by_precio(400, 600)
        self.assertIn(producto_1, productos_rango_precio)
        self.assertNotIn(producto_2, productos_rango_precio)

    # Agrega más pruebas para otros métodos y funcionalidades del modelo Producto

class OpinionModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.categoria = Categoria.objects.create(nombre='Electrónica')
        self.fabricante = Fabricante.objects.create(nombre='Sony')
        self.producto = Producto.objects.create(
            categoria=self.categoria,
            fabricante=self.fabricante,
            nombre='Televisor',
            precio=500,
            cantidad=10
        )
        
    def test_opinion_str(self):
        opinion = Opinion.objects.create(
            producto=self.producto,
            user=self.user,
            tu_opinion='Este producto es genial.'
        )
        self.assertEqual(str(opinion), f"{opinion.producto.nombre}: {opinion.user.username}")
        
    # Agrega más pruebas para otras funcionalidades del modelo Opinion

# Añade pruebas para el ProductoManager si tiene métodos personalizados que necesiten ser probados
