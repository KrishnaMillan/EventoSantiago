from django.shortcuts import render, render_to_response, redirect
from django.template import loader
from django.http import HttpResponse
from .forms import AgregaUsuario, Login
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

	if form.is_valid():
		data=form.cleaned_data

		nombre=data.get("nombre")
		rut=data.get("rut")
		contrasena=data.get("contrasena")
		correoAsociado=data.get("correoAsociado")
		#tipo_usuario="Usuario"

		esActiva=True
		fec_nac=data.get("fec_nac")
		fecha_registro=time.strftime("%Y-%m-%d")
		cuenta=Cuenta(rut=rut, nombre=nombre, correoAsociado=correoAsociado, esactiva=esActiva, fecha_registro=fecha_registro)
		cuenta.save()
		usuario=Usuario(Cuenta=cuenta, fec_nac=fec_nac)
		usuario.save()
		user=User.objects.create_user(username=rut,password=contrasena)
		user.save()
		try:
			user.groups.add(Group.objects.get(name="Usuarios"))
		except Group.DoesNotExist:
			Group.objects.create(name="Usuarios")
			user.groups.add(Group.objects.get(name="Usuarios"))
	return render(request, "registrarse.html",{'form':form})


def ingresar(request):
	form=Login(request.POST or None)
	if form.is_valid():
		data=form.cleaned_data
		user=authenticate(username=data.get("rut"),password=data.get("contrasena"))
		if user is not None:
			login(request, user)
			return redirect('index')
	return render(request,"login.html",{'form':form})

def salir(request):
	logout(request)
	return redirect("/")
