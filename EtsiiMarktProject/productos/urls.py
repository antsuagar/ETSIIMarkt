from django.contrib import admin
from django.urls import include, path
from .views import catalogo
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [    

    #path("admin/", admin.site.urls),
    path("catalogo/", catalogo, name='catalogo'),
]
