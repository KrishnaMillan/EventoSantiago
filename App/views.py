from django.shortcuts import render, render_to_response, redirect
from django.template import loader
from django.http import HttpResponse
from .forms import AgregaUsuario, Login, ActualizaUsuario
from .models import Cuenta, Usuario
import time
from django.contrib.auth.models  import Group, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
	if form.is_valid():
		data=form.cleaned_data
		cuenta=Cuenta.objects.get(rut=data.get("rut"))
		user=authenticate(username=data.get("rut"),password=data.get("contrasena"))
		activo=User.objects.get(username=data.get("rut"))
		if activo and user is not None:
			login(request, user)
			return redirect('index')
	return render(request,"login.html",{'form':form})

def salir(request):
	logout(request)
	return redirect("/")

@login_required(login_url='ingresar')
def micuenta(request):
	usuario=Usuario.objects.filter(Cuenta=(Cuenta.objects.get(rut=request.user.get_username())))

	if request.POST.get("eliminar") is not None:
		request.user.is_active=False
		logout(request)
		return redirect("/")


	return render(request,"micuenta.html",{'usuario':usuario})

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
