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
]