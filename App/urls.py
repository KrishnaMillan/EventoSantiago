from django.urls import path
from . import views
from django.conf.urls import url, include
urlpatterns=[
    path('',views.index, name="index"),
    path('registrarse',views.registrarse, name="registrarse"),
    path('login',views.ingresar, name="login"),
    path('salir',views.salir, name="salir"),
    path('micuenta',views.micuenta, name="micuenta"),
    path('actualizar',views.actualizar, name="actualizar"),
    path('eliminar',views.eliminar, name="eliminar"),
    path('recuperar',views.recuperar, name="recuperar"),
    path('recuperarcontrasena',views.recuperarcontrasena, name="recuperarcontrasena"),
    path('cambiarcontrasena',views.cambiarcontrasena, name="cambiarcontrasena"),
    path('reactivar',views.reactivar, name="reactivar"),
]