from django.urls import path
from . import views
from django.conf.urls import url, include
urlpatterns=[
    path('',views.index, name="index"),
    path('registrarse',views.registrarse, name="registrarse"),
    path('ingresar',views.ingresar, name="ingresar"),
    path('salir',views.salir, name="salir"),
    path('micuenta',views.micuenta, name="micuenta"),
    path('actualizar',views.actualizar, name="actualizar"),
    path('eliminar',views.eliminar, name="eliminar"),
    path('recuperar',views.recuperar, name="recuperar"),
    path('recuperarcontrasena',views.recuperarcontrasena, name="recuperarcontrasena"),
    path('cambiarcontrasena',views.cambiarcontrasena, name="cambiarcontrasena"),
    path('reactivar',views.reactivar, name="reactivar"),
    path('registroEmpresa',views.registroEmpresa, name="registroEmpresa"),
    path('solicitudEmpresas',views.solicitudEmpresas, name="solicitudEmpresas"),
    path('detalleEmpresa',views.detalleEmpresa, name="detalleEmpresa"),
    path('creaAdmin',views.creaAdmin, name="creaAdmin"),
    path('eliminaAdmin',views.eliminaAdmin, name="eliminaAdmin"),
    path('misEventos', views.misEventos, name="misEventos"),
    path('eliminarEvento/<id_evento>/', views.eliminarEvento, name="eliminarEvento"),
    path('crearEvento', views.crearEvento, name="crearEvento"),
    path('modificarEvento/<id_evento>/', views.modificarEvento, name="modificarEvento"),
    path('misReservas', views.misReservas, name="misReservas"),
    path('configuraEmpresa',views.configuraEmpresa, name="configuraEmpresa"),
    path('modificaEmpresa',views.modificaEmpresa, name="modificaEmpresa"),
]