from django.shortcuts import render, render_to_response, redirect
from django.template import loader
from django.http import HttpResponse
from .forms import AgregaUsuario, Login, ActualizaUsuario, RecuperaContrasena, RecuperaContrasena2
from .models import Cuenta, Usuario
import time
from django.contrib.auth.models  import Group, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, send_mail

# Create your views here.
def index(request):
	return render(request, "index.html")

def registrarse(request):
	form=AgregaUsuario(request.POST or None)
	mensaje=""
	if form.is_valid():
		data=form.cleaned_data

		nombre=data.get("nombre")
		rut=data.get("rut")
		contrasena=data.get("contrasena")
		contrasena2=data.get("contrasena2")
		correoAsociado=data.get("correoAsociado")
		comuna=data.get("comuna")
		fec_nac=data.get("fec_nac")
		fecha_registro=time.strftime("%Y-%m-%d")
		if contrasena==contrasena2:
			cuenta=Cuenta(rut=rut, nombre=nombre, correoAsociado=correoAsociado,comuna=comuna, fecha_registro=fecha_registro)
			cuenta.save()
			usuario=Usuario(Cuenta=cuenta, fec_nac=fec_nac)
			usuario.save()
			user=User.objects.create_user(username=rut,password=contrasena,is_active=True)
			user.save()
			mensaje="Usuario agregado correctamente"
			try:
				user.groups.add(Group.objects.get(name="Usuarios"))
			except Group.DoesNotExist:
				Group.objects.create(name="Usuarios")
				user.groups.add(Group.objects.get(name="Usuarios"))
		else: 
			mensaje="Las contraseñas no coinciden"
	return render(request, "registrarse.html",{'form':form, 'mensaje':mensaje})


def ingresar(request):
	form=Login(request.POST or None)
	mensaje=""
	if form.is_valid():
		data=form.cleaned_data
		cuenta=Cuenta.objects.get(rut=data.get("rut"))
		correo=cuenta.correoAsociado
		user=authenticate(username=data.get("rut"),password=data.get("contrasena"))
		users=User.objects.get(username=data.get("rut"))
		if user is not None:
				login(request, user)
				return redirect('index')

		else:
			if users.is_active==False:
				mensaje="Tu cuenta está inactiva, se envió un link a tu correo electrónico para reactivarla"
				send_mail('Reactiva tu cuenta','','eventosantiago7@gmail.com',[correo],html_message='Este email fue enviado porque tu cuenta está inactiva e intentaste iniciar sesión <br><a href="http://127.0.0.1:8000/reactivar?user='+users.username+'">Click aquí para reactivar tu cuenta</a><br>si no fuiste tu ignora este email')
				return redirect('/')	
			
	return render(request,"login.html",{'form':form, 'mensaje':mensaje})

def salir(request):
	logout(request)
	return redirect("/")

@login_required(login_url='ingresar')
def micuenta(request):
	usuario=Usuario.objects.filter(Cuenta=(Cuenta.objects.get(rut=request.user.get_username())))
	return render(request,"micuenta.html",{'usuario':usuario})
@login_required(login_url='ingresar')
def eliminar(request):
	user=User.objects.get(username=request.user.get_username())
	user.is_active=False
	user.save()
	logout(request)
	return redirect("/")
def actualizar(request):
	mensaje=""
	form=ActualizaUsuario(request.POST or None)
	
	x=False;
	if form.is_valid():
		data=form.cleaned_data
		nombre=data.get("nombre")
		correoAsociado=data.get("correoAsociado")
		fec_nac=data.get("fec_nac")
		comuna=data.get("comuna")
		if(nombre!= ""):
			Cuenta.objects.filter(rut=request.user.get_username()).update(nombre=nombre)
			x=True
		if(correoAsociado!= ""):
			Cuenta.objects.filter(rut=request.user.get_username()).update(correoAsociado=correoAsociado)
			x=True
		if(fec_nac!= None):
			Usuario.objects.filter(Cuenta=(Cuenta.objects.get(rut=request.user.get_username()))).update(fec_nac=fec_nac)
			x=True
		if(comuna!= ""):
			Usuario.objects.filter(Cuenta=(Cuenta.objects.get(rut=request.user.get_username()))).update(comuna=comuna)
			x=True
		if x:
			mensaje="Datos actualizados correctamente"

	return render(request,"actualizar.html",{'form':form,'mensaje':mensaje})

def recuperar(request):
	form=RecuperaContrasena(request.POST or None)
	if form.is_valid():
		data=form.cleaned_data
		rut=data.get("rut")
		cuenta=Cuenta.objects.get(rut=rut)
		correo=cuenta.correoAsociado
		send_mail('Recuperar Contraseña','','eventosantiago7@gmail.com',[correo],html_message='Este email fue enviado porque solicitaste recuperar tu contraseña<br><a href="http://127.0.0.1:8000/recuperarcontrasena?user='+rut+'">Click aquí para recuperar contraseña</a><br>si no fuiste tu ignora este email')
	return render(request,"recuperar.html",{'form':form})

def recuperarcontrasena(request):
	form=RecuperaContrasena2(request.POST or None)
	if form.is_valid():
		data=form.cleaned_data
		contrasena=data.get("contrasena")
		contrasena2=data.get("contrasena2")
		if contrasena==contrasena2:
			usuario=User.objects.get(username=request.GET.get("user"))
			usuario.set_password(contrasena)
			usuario.save()
	return render(request,"recuperar.html",{'form':form})


@login_required(login_url='ingresar')
def cambiarcontrasena(request):
	form=RecuperaContrasena2(request.POST or None)
	if form.is_valid():
		data=form.cleaned_data
		contrasena=data.get("contrasena")
		contrasena2=data.get("contrasena2")
		if contrasena==contrasena2:
			usuario=User.objects.get(username=request.user.get_username())
			usuario.set_password(contrasena)
			usuario.save()
		else:
			mensaje="las contraseñas no coinciden"
	return render(request,"cambiarcontrasena.html",{'form':form})

def reactivar(request):
	usuario=User.objects.get(username=request.GET.get("user"))
	usuario.is_active=True
	usuario.save()
	return render(request,"reactivar.html")
