"""
URL configuration for EtsiiMarkt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
#from clientes.views import RegistroClienteView
from clientes.views import IniciarSesionView, editar_direccion_envio, editar_mi_tarjeta, logout_personalizado, modificar_datos_usuario, perfil, register
from django.contrib.auth.views import LogoutView
from core.views import index, nosotros, devoluciones
from productos.views import catalogo, catalogo2
from pedidos.views import actualizar, eliminar, formulario_envio, procesar_pedido, pedidos_usuario, error
from pedidos.views import agregar_reclamacion, editar_reclamacion, reclamaciones_cliente, eliminar_reclamacion
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('productos/', include('productos.urls')),
    path('catalogo/', catalogo, name='catalogo'),
    path('busqueda/', catalogo2, name='catalogo2'),
    path('login/', IniciarSesionView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registro/', register, name='registro_usuario'),
    path('perfil/', perfil, name='perfil_usuario'),
    path('modificar_perfil/', modificar_datos_usuario, name='modificar_perfil'),
    path('actualizar/<int:producto_id>/', actualizar, name='actualizar'),
    path('eliminar/<int:producto_id>/', eliminar, name='eliminar'),
    path('formulario_envio/<int:pedido_id>/', formulario_envio, name='formulario_envio'),
    path('pedido_realizado/', procesar_pedido, name='procesar_pedido'),
    path('seguimiento/', pedidos_usuario, name='seguimiento'),
    path('error/<str:error>/', error, name='error'),
    path('pedido/<int:pedido_id>/agregar-reclamacion/', agregar_reclamacion, name='agregar_reclamacion'),
    path('pedido/<int:reclamacion_id>/editar_reclamacion/', editar_reclamacion, name='editar_reclamacion'),
    path('pedido/<int:reclamacion_id>/eliminar_reclamacion/', eliminar_reclamacion, name='eliminar_reclamacion'),
    path('pedido/reclamaciones_cliente/', reclamaciones_cliente, name='reclamaciones_cliente'),
    path('nosotros', nosotros, name='nosotros'),
    path('devoluciones', devoluciones, name='devoluciones'),
    path('logout_personalizado', logout_personalizado, name='logout_personalizado'),
    path('clientes/direccion_envio/', editar_direccion_envio, name='editar_direccion_envio'),
    path('clientes/tarjeta/', editar_mi_tarjeta, name='editar_mi_tarjeta'),
]
    

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
