from django.shortcuts import render, render_to_response, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .forms import Login
from .models import Cuenta, Usuario, RegistroEmail, Empresa, Administrador, Evento, Reserva, Visita
import datetime, time
import uuid
from datetime import timedelta, date
from django.contrib.auth.models  import Group, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, send_mail

# Create your views here.
def index(request):
	return render(request, "index.html")

def registrarse(request):
	mensaje=""
	if request.POST:
		nombre=request.POST.get("nombre")
		rut=request.POST.get("rut")
		contrasena=request.POST.get("contrasena")
		contrasena2=request.POST.get("contrasena2")
		correoAsociado=request.POST.get("correoAsociado")
		comuna=request.POST.get("comuna")
		fec_nac=request.POST.get("fec_nac")
		fecha_registro=time.strftime("%Y-%m-%d")
		try:
			user=User.objects.get(username=rut)
			mensaje="Este rut ya está registrado, ingrese los datos nuevamente"
		except:
			if contrasena==contrasena2:
				
				user=User.objects.create_user(username=rut,password=contrasena,is_active=True)
				user.save()
				cuenta=Cuenta(rut=rut, nombre=nombre, correoAsociado=correoAsociado, user=user, comuna=comuna, fecha_registro=fecha_registro)
				cuenta.save()
				usuario=Usuario(Cuenta=cuenta, fec_nac=fec_nac)
				usuario.save()
				mensaje="Usuario agregado correctamente"
				try:
					user.groups.add(Group.objects.get(name="Usuarios"))
				except Group.DoesNotExist:
					Group.objects.create(name="Usuarios")
					user.groups.add(Group.objects.get(name="Usuarios"))
			else: 
				mensaje="Las contraseñas no coinciden"
			

	return render(request, "registrarse.html",{'mensaje':mensaje})


def ingresar(request):
	form=Login(request.POST or None)
	mensaje=""
	try:
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
				mensaje="Tu usuario o contraseña es incorrecta, intenta nuevamente!!"
			if users.is_active==False and User.objects.filter(username=data.get("rut"), groups__name='Usuarios').exists():
				iduuid=str(uuid.uuid4())
				registro=RegistroEmail(Cuenta=cuenta, iduuid=iduuid)
				registro.save()
				mensaje="Tu cuenta está inactiva, se envió un link a tu correo electrónico para reactivarla"
				send_mail('Reactiva tu cuenta','','eventosantiago7@gmail.com',[correo],html_message='Este email fue enviado porque tu cuenta está inactiva e intentaste iniciar sesión <br><a href="http://krishnamillan.pythonanywhere.com/reactivar?iduuid='+iduuid+'&user='+users.username+'">Click aquí para reactivar tu cuenta</a><br>si no fuiste tu ignora este email')	
			if users.is_active==False and User.objects.filter(username=data.get("rut"), groups__name='Empresas').exists():
				mensaje="Tu cuenta de empresa, aún no ha sido activada"
				
	except:
		mensaje="No se ha encontrado el usuario"
			
	return render(request,"login.html",{'form':form, 'mensaje':mensaje})

def salir(request):
	logout(request)
	return redirect("/")

@login_required(login_url='ingresar')
def micuenta(request):
	if User.objects.filter(username=request.user.get_username(), groups__name='Usuarios').exists():
		usuario=Usuario.objects.filter(Cuenta=(Cuenta.objects.get(rut=request.user.get_username())))
	if User.objects.filter(username=request.user.get_username(), groups__name='Empresas').exists():
		usuario=Empresa.objects.filter(Cuenta=(Cuenta.objects.get(rut=request.user.get_username())))
	if User.objects.filter(username=request.user.get_username(), groups__name='Administradores').exists():
		usuario=Administrador.objects.filter(Cuenta=(Cuenta.objects.get(rut=request.user.get_username())))
	return render(request,"micuenta.html",{'usuario':usuario})
@login_required(login_url='ingresar')
def eliminar(request):
	user=User.objects.get(username=request.user.get_username())
	user.is_active=False
	user.save()
	mensaje="Desactivada"
	logout(request)
	return render(request,'index.html', {'mensaje':mensaje})
@login_required(login_url='ingresar')
def actualizar(request):
	mensaje=""
	usuario=Usuario.objects.filter(Cuenta=(Cuenta.objects.get(rut=request.user.get_username())))
	cuenta=Cuenta.objects.get(rut=request.user.get_username())
	if request.method=='POST':
		nombre=request.POST.get("nombre")
		correoAsociado=request.POST.get("correoAsociado")
		comuna=request.POST.get("comuna")
		mensaje="Todos los campos estan en blanco, no se han realizado cambios"
		
		if(nombre!=None and nombre!=""):
			Cuenta.objects.filter(rut=request.user.get_username()).update(nombre=nombre)
			mensaje="Datos actualizados correctamente"
			
		if(correoAsociado!=None and correoAsociado!=""):
			Cuenta.objects.filter(rut=request.user.get_username()).update(correoAsociado=correoAsociado)
			mensaje="Datos actualizados correctamente"
			
		if(comuna!=None and comuna!=""):
			Cuenta.objects.filter(rut=request.user.get_username()).update(comuna=comuna)
			mensaje="Datos actualizados correctamente"
			
	return render(request,"actualizar.html",{'usuario':usuario,'mensaje':mensaje})

def recuperar(request):
	mensaje=""
	iduuid=str(uuid.uuid4())
	if request.POST:
		rut=request.POST.get("rut")
		try:
			if User.objects.filter(username=rut, groups__name='Usuarios').exists():
				cuenta=Cuenta.objects.get(rut=rut)
				correo=cuenta.correoAsociado
				send_mail('Recuperar Contraseña','','eventosantiago7@gmail.com',[correo],html_message='Este email fue enviado porque solicitaste recuperar tu contraseña<br><a href="http://krishnamillan.pythonanywhere.com/recuperarcontrasena?iduuid='+iduuid+'&user='+rut+'">Click aquí para recuperar contraseña</a><br>si no fuiste tu ignora este email')
				mensaje="Se ha enviado un correo a su mail asociado"
				registro=RegistroEmail(Cuenta=cuenta, iduuid=iduuid)
				registro.save()
			else:
				mensaje="Tu cuenta es una cuenta de empresa, si necesitas recuperar tu contraseña, ponte en contacto con el administrador"
		except Cuenta.DoesNotExist:
			mensaje="No se encuentra el rut"
	return render(request,"recuperar.html",{'mensaje':mensaje})

def recuperarcontrasena(request):
	existe=True
	mensaje=""
	try:
		if User.objects.filter(username=request.GET.get("user"), groups__name='Usuarios').exists():
			cuenta=Cuenta.objects.get(rut=request.GET.get("user"))
			registro=RegistroEmail.objects.get(Cuenta=cuenta, iduuid=request.GET.get("iduuid"))
			if request.POST:
				contrasena=request.POST.get("contrasena1")
				contrasena2=request.POST.get("contrasena2")
				if contrasena==contrasena2:
					usuario=User.objects.get(username=request.GET.get("user"))
					usuario.set_password(contrasena)
					usuario.save()
					mensaje="Contraseña actualizada correctamente"
					registro.delete()
				else:
					mensaje="Las contraseñas no coinciden"
		else:
			mensaje="Tu cuenta es una cuenta de empresa"
	except:
		existe=False
	return render(request,"recuperarcontrasena.html",{'mensaje':mensaje, 'existe':existe})


@login_required(login_url='ingresar')
def cambiarcontrasena(request):
	mensaje=""
	usuario=User.objects.get(username=request.user.get_username())
	if request.POST:
		contrasena=request.POST.get("contrasena1")
		contrasena2=request.POST.get("contrasena2")
		usuario=User.objects.get(username=request.user.get_username())
		
		if(usuario.check_password(request.POST.get('actual'))):
			if contrasena==contrasena2:
				usuario.set_password(contrasena)
				usuario.save()
				mensaje="Contraseña cambiada correctamente, se cerrarán todas tus sesiones"
			else:
				mensaje="las contraseñas no coinciden"
		else:
			mensaje="La contraseña actual es incorrecta"
	return render(request,"cambiarcontrasena.html",{'mensaje':mensaje})

def reactivar(request):
	existe=True
	try:
		if User.objects.filter(username=request.GET.get("user"), groups__name='Usuarios').exists():
			cuenta=Cuenta.objects.get(rut=request.GET.get("user"))
			registro=RegistroEmail.objects.get(Cuenta=cuenta, iduuid=request.GET.get("iduuid"))
			usuario=User.objects.get(username=request.GET.get("user"))
			usuario.is_active=True
			usuario.save()
			registro.delete()
		else:
			existe=False
	except:
		existe=False


	return render(request,"reactivar.html",{'existe':existe})


#
def registroEmpresa(request):
	mensaje=""
	if request.POST:
		nombre=request.POST.get("nombre")
		rut=request.POST.get("rut")
		contrasena=request.POST.get("contrasena")
		contrasena2=request.POST.get("contrasena2")
		correoAsociado=request.POST.get("correoAsociado")
		comuna=request.POST.get("comuna")
		direccion=request.POST.get("direccion")
		fecha_registro=time.strftime("%Y-%m-%d")
		try:
			user=User.objects.get(username=rut)
			mensaje="Este rut ya está registrado, ingrese los datos nuevamente"
		except:
			if contrasena==contrasena2:
				
				user=User.objects.create_user(username=rut,password=contrasena,is_active=False)
				user.save()
				cuenta=Cuenta(rut=rut, nombre=nombre, correoAsociado=correoAsociado, user=user, comuna=comuna, fecha_registro=fecha_registro)
				cuenta.save()
				empresa=Empresa(Cuenta=cuenta, direccion=direccion)
				empresa.save()
				mensaje="Solicitud enviada correctamente"
				try:
					user.groups.add(Group.objects.get(name="Empresas"))
				except Group.DoesNotExist:
					Group.objects.create(name="Empresas")
					user.groups.add(Group.objects.get(name="Empresas"))
			else: 
				mensaje="Las contraseñas no coinciden"
			

	return render(request, "registroempresa.html",{'mensaje':mensaje})

@login_required(login_url='ingresar')
def creaAdmin(request):
	mensaje=""
	if request.POST:
		nombre=request.POST.get("nombre")
		rut=request.POST.get("rut")
		contrasena=request.POST.get("contrasena")
		contrasena2=request.POST.get("contrasena2")
		correoAsociado=request.POST.get("correoAsociado")
		comuna=request.POST.get("comuna")
		fec_nac=request.POST.get("fec_nac")
		fec_ingreso=request.POST.get("fec_ingreso")
		fecha_registro=time.strftime("%Y-%m-%d")
		try:
			user=User.objects.get(username=rut)
			mensaje="Este rut ya está registrado, ingrese los datos nuevamente"
		except:
			if contrasena==contrasena2:
				
				user=User.objects.create_user(username=rut,password=contrasena,is_active=True)
				user.save()
				cuenta=Cuenta(rut=rut, nombre=nombre, correoAsociado=correoAsociado, user=user, comuna=comuna, fecha_registro=fecha_registro)
				cuenta.save()
				administrador=Administrador(Cuenta=cuenta, fec_nac=fec_nac, fec_ingreso=fec_ingreso)
				administrador.save()
				mensaje="Administrador agregado correctamente"
				try:
					user.groups.add(Group.objects.get(name="Administradores"))
				except Group.DoesNotExist:
					Group.objects.create(name="Administradores")
					user.groups.add(Group.objects.get(name="Administradores"))
			else: 
				mensaje="Las contraseñas no coinciden"
	return render(request,"creaadmin.html",{'mensaje':mensaje})

@login_required(login_url='ingresar')
def solicitudEmpresas(request):
	cuentas=Cuenta.objects.filter(user__in=User.objects.filter(groups__name='Empresas', is_active=False))
	return render(request,"solicitudempresas.html",{'cuentas':cuentas})

@login_required(login_url='ingresar')
def detalleEmpresa(request):
	
	
	cuenta=Cuenta.objects.get(rut=request.GET.get("rut"))

	mensaje=""
	visitas="No tiene visitas agendadas"
	existe=False
	
	if(Visita.objects.filter(Empresa=(Empresa.objects.get(Cuenta=cuenta))).exists()):
		visita=Visita.objects.get(Empresa=(Empresa.objects.get(Cuenta=cuenta)))
		visitas=visita.fecha_visita
		existe=True
	else:
		if request.POST.get("agendarVisita") is not None:
			rut=request.POST.get("rut")
			fecha_visita= datetime.date.today() + timedelta(days=1)
			visita=Visita(fecha_visita=fecha_visita,Empresa=Empresa.objects.get(Cuenta=cuenta), Administrador=Administrador.objects.get(Cuenta=Cuenta.objects.get(rut=request.user.get_username())))
			visita.save()
			mensaje="Visita guardada correctamente"
	if request.POST.get("activar") is not None and existe:
		rut=request.POST.get("rut")
		user=User.objects.get(username=rut)
		
		if Visita.objects.filter(Empresa=(Empresa.objects.get(Cuenta=cuenta)), Administrador=Administrador.objects.get(Cuenta=Cuenta.objects.get(rut=request.user.get_username()))).exists():
			resolucion=request.POST.get("resolucion")
			fec_activacion=datetime.date.today()
			Empresa.objects.filter(Cuenta=cuenta).update(fec_activacion=fec_activacion)
			Visita.objects.filter(Empresa=Empresa.objects.get(Cuenta=cuenta), Administrador=(Administrador.objects.get(Cuenta=(Cuenta.objects.get(rut=request.user.get_username()))))).update(resolucion=resolucion)
		
			
			user.is_active=True
			user.save()
			mensaje="Cuenta activada correctamente"
		
		
	

	return render(request,"detalleempresa.html",{'existe':existe,'cuenta':cuenta,'mensaje':mensaje, 'visitas':visitas})
