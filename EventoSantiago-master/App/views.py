from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import Login
from .models import Cuenta, Usuario, RegistroEmail, Empresa, Administrador, Evento, Reserva, Visita
import datetime, time
import uuid
import string
from datetime import timedelta, date
from django.contrib.auth.models  import Group, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, send_mail
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.
def index(request):
	return render(request, "index.html")
@login_required
def configuraEmpresa(request):
	empresa=User.objects.filter(groups__name='Empresas')
	empresas=Cuenta.objects.filter(user__in=User.objects.filter(groups__name='Empresas'))
	mensaje=""

	if request.POST.get("activar") is not None:
		user=User.objects.get(username=request.POST.get("rut"))
		user.is_active=True
		user.save()
		mensaje="Cuenta activada correctamente"
	if request.POST.get("eliminar") is not None:
		user=User.objects.get(username=request.POST.get("rut"))
		user.is_active=False
		user.save()
		mensaje="Cuenta desactivada correctamente"
	if request.POST.get("modificar") is not None:
		mensaje=""
		cuenta=Cuenta.objects.get(rut=request.POST.get("rut"))
		empresa=Empresa.objects.get(Cuenta=cuenta)
		return render(request, 'modificaempresa.html',{'cuenta':cuenta, 'empresa':empresa,'mensaje':mensaje})
	return render(request, "configuraempresa.html", {'mensaje':mensaje,'empresa':empresa,'empresas':empresas})

def modificaEmpresa(request):
	cuenta=Cuenta.objects.get(rut=request.POST.get("rut"))
	user=User.objects.get(username=request.POST.get("rut"))
	empresa=Empresa.objects.get(Cuenta=cuenta)
	user.set_password(request.POST.get("contrasena"))
	user.save()
	cuenta.correoAsociado=request.POST.get("correoAsociado")
	cuenta.comuna=request.POST.get("comuna")
	empresa.direccion=request.POST.get("direccion")
	cuenta.save()
	empresa.save()
	mensaje="Modificado correctamente"
	return render(request, 'modificaempresa.html',{'cuenta':cuenta, 'empresa':empresa,'mensaje':mensaje})


def FiltroEvento(request):
	Eve = Evento.objects.all()
	filtro = request.POST.get('comunaf')
	if request.POST.get("comunaf") is not None:
		Eve = Evento.objects.filter(comuna=filtro)
	if request.POST.get("comunaf") == 'Todas':
		Eve = Evento.objects.all()
		
	if request.POST.get("reservarEvento") is not None:
		try:
			evento = Evento.objects.get(id_evento=request.POST.get("idevento"))
			reservaevento=Reserva.objects.filter(Evento=evento).count()
			usuario= Usuario.objects.get(Cuenta=Cuenta.objects.get(rut=request.user.get_username()))
			fecha=datetime.date.today().strftime("%Y-%m-%d")
			hora=datetime.datetime.now().strftime("%H:%M:%S")
			if(int(evento.cant_cupos)>reservaevento+1):
				reserva=Reserva(fecha=fecha, hora=hora, Evento=evento, Usuario=usuario)
				reserva.save()
				mensaje="Ticket generado correctamente"
				messages.success(request, mensaje)
			else:
				mensaje = "Error al reservar, no hay cupos!!!!"
				messages.error(request, mensaje)

		except:
			mensaje = "Error al reservar"
			messages.error(request, mensaje)

	return render(request, 'FiltroEvento.html', {'Eve':Eve, 'filtro':filtro})


@login_required(login_url='ingresar')
def misReservas(request):
	reservas=Reserva.objects.filter(Usuario=Usuario.objects.get(Cuenta=Cuenta.objects.get(rut=request.user.get_username())))
	if request.POST.get("cancelarReserva") is not None:
		try:
			reserva=Reserva.objects.get(id_reserva=request.POST.get("idreserva"))
			reserva.delete()
			mensaje="Ticket eliminado correctamente"
			messages.success(request, mensaje)
		except:
			mensaje = "Error al cancelar"
			messages.error(request, mensaje)

	return render(request, 'misreservas.html',{'reservas':reservas})
@login_required(login_url='ingresar')
def misEventos(request):
	event = Evento.objects.all()
	misevents=""
	if User.objects.filter(username=request.user.get_username(), groups__name='Empresas').exists():
		misevents=Evento.objects.filter(Empresa=Empresa.objects.get(Cuenta=Cuenta.objects.get(rut=request.user.get_username())))
	if request.POST.get("reservarEvento") is not None:
		try:
			evento = Evento.objects.get(id_evento=request.POST.get("idevento"))
			reservaevento=Reserva.objects.filter(Evento=evento).count()
			usuario= Usuario.objects.get(Cuenta=Cuenta.objects.get(rut=request.user.get_username()))
			fecha=datetime.date.today().strftime("%Y-%m-%d")
			hora=datetime.datetime.now().strftime("%H:%M:%S")
			if(int(evento.cant_cupos)>reservaevento+1):
				reserva=Reserva(fecha=fecha, hora=hora, Evento=evento, Usuario=usuario)
				reserva.save()
				mensaje="Ticket generado correctamente"
				messages.success(request, mensaje)
			else:
				mensaje = "Error al reservar, no hay cupos!!!!"
				messages.error(request, mensaje)

		except:
			mensaje = "Error al reservar"
			messages.error(request, mensaje)
	return render(request, 'miseventos.html', {'event':event, 'misevents':misevents})
@login_required(login_url='ingresar')
def eliminarEvento(request, id_evento):
	event = Evento.objects.get(id_evento = id_evento)
	try:
		event.estado=False
		event.save()
		mensaje = "Evento Eliminado Correctamente"
		messages.success(request, mensaje)
	except:
		mensaje = "Error al eliminar"
		messages.error(request, mensaje)
	return redirect('misEventos')
@login_required(login_url='ingresar')
def crearEvento(request):
	variables = {}
	variables['mensaje']=''
	if request.POST:
		event = Evento()
		event.fecha = request.POST.get('fecha')
		event.hora = datetime.datetime.strptime(request.POST.get('hora'),"%H:%M")
		event.comuna = request.POST.get('comuna')
		event.nombre=request.POST.get('nombre')
		event.descripcion=request.POST.get('descripcion')
		event.direccion = request.POST.get('direccion')
		event.cant_cupos = request.POST.get('cupos')
		event.pagReserva = request.POST.get('pagReserva')
		event.Empresa = Empresa.objects.get(Cuenta=Cuenta.objects.get(rut=request.user.get_username()))
		try:
			event.save()
			variables['mensaje'] = 'Evento Guardado'
		except:
			variables['mensaje'] = 'Error al guardar'
	return render(request, 'crearEvento.html', variables)

@login_required(login_url='ingresar')
def modificarEvento(request, id_evento):
	event = Evento.objects.get(id_evento = id_evento)
	event.fecha=event.fecha.strftime("%Y-%m-%d")
	variables = {
		'event':event
	}

	if request.POST:
		event = Evento()
		event.id_evento = request.POST.get('id')
		event.fecha = request.POST.get('fecha')
		event.hora = request.POST.get('hora')
		event.comuna = request.POST.get('comuna')
		event.nombre=request.POST.get('nombre')
		event.descripcion=request.POST.get('descripcion')
		event.direccion = request.POST.get('direccion')
		event.cant_cupos = request.POST.get('cupos')
		event.pagReserva = request.POST.get('pagReserva')
		event.Empresa = Empresa.objects.get(Cuenta=Cuenta.objects.get(rut=request.user.get_username()))
		try:
			event.save()
			messages.success(request, 'Modificado correctamente')
		except:
			messages.error(request, 'Error')
		return redirect('misEventos')

	return render(request, 'modificarEvento.html', variables)

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
	return render(request,"login.html",{'form':form,'mensaje':mensaje})


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
	if User.objects.filter(username=request.user.get_username(), groups__name='Usuarios').exists():
	    usuario=Reserva.objects.filter(Usuario=Usuario.objects.get(Cuenta=Cuenta.objects.get(rut=request.user.get_username())))
	    usuario.delete()
	    mensaje="Desactivada"

	if User.objects.filter(username=request.user.get_username(), groups__name='Empresas').exists():
		visita=Visita.objects.get(Empresa=(Empresa.objects.get(Cuenta=Cuenta.objects.get(rut=request.user.get_username()))))
		visita.resolucion="La cuenta fue desactivada el: "+ time.strftime("%Y-%m-%d")
		visita.save()
		mensaje="Empresa Desactivada"

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
			if User.objects.filter(username=rut, groups__name='Empresas').exists():
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


#Zona de empresa
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
def eliminaAdmin(request):
	usuario=User.objects.filter(groups__name='Administradores')
	administradores=Cuenta.objects.filter(user__in=User.objects.filter(groups__name='Administradores'))
	mensaje=""
	if request.POST.get("activar") is not None:
		user=User.objects.get(username=request.POST.get("rut"))
		user.is_active=True
		user.save()
		mensaje="Cuenta activada correctamente"
	if request.POST.get("eliminar") is not None:
		user=User.objects.get(username=request.POST.get("rut"))
		user.is_active=False
		user.save()
		mensaje="Cuenta desactivada correctamente"
	return render(request,"eliminaadmin.html",{'mensaje':mensaje,'administradores':administradores, 'usuario':usuario})


@login_required(login_url='ingresar')
def solicitudEmpresas(request):
	mensaje=""
	cuentas=Cuenta.objects.filter(user__in=User.objects.filter(groups__name='Empresas', is_active=False))
	return render(request,"solicitudempresas.html",{'cuentas':cuentas,'mensaje':mensaje})


@login_required(login_url='ingresar')
def verCuentas(request):
	mensaje=""
	usuario=User.objects.filter(groups__name='Empresas')
	empresas=Cuenta.objects.filter(user__in=User.objects.filter(groups__name='Empresas'))
	usuu=User.objects.filter(groups__name='Usuarios')
	usu=Cuenta.objects.filter(user__in=User.objects.filter(groups__name='Usuarios'))
	return render(request,"verCuentas.html",{'mensaje':mensaje,'empresas':empresas, 'usuario':usuario, 'usuu':usuu, 'usu':usu})


@login_required(login_url='ingresar')
def detalleEmpresa(request):

	cuentas=Cuenta.objects.filter(user__in=User.objects.filter(groups__name='Empresas', is_active=False))
	cuenta=Cuenta.objects.get(rut=request.GET.get("rut"))
	resolucion=""
	mensaje=""
	visitas="No tiene visitas agendadas"
	existe=False

	if(Visita.objects.filter(Empresa=(Empresa.objects.get(Cuenta=cuenta))).exists()):
		visita=Visita.objects.get(Empresa=(Empresa.objects.get(Cuenta=cuenta)))
		visitas=visita.fecha_visita
		if(visita.resolucion!=""):
			resolucion=visita.resolucion
		existe=True
	else:
		if request.POST.get("agendarVisita") is not None:
			rut=request.POST.get("rut")
			fecha_visita= datetime.date.today() + timedelta(days=1)
			visita=Visita(fecha_visita=fecha_visita,Empresa=Empresa.objects.get(Cuenta=cuenta), Administrador=Administrador.objects.get(Cuenta=Cuenta.objects.get(rut=request.user.get_username())), resolucion="")
			visita.save()
			mensaje="Visita guardada correctamente"
			return render(request,"solicitudempresas.html",{'mensaje':mensaje,'cuentas':cuentas})
	if request.POST.get("guardarResolucion") is not None and existe:
		resolucion=request.POST.get("resolucion")
		Visita.objects.filter(Empresa=Empresa.objects.get(Cuenta=cuenta), Administrador=(Administrador.objects.get(Cuenta=(Cuenta.objects.get(rut=request.user.get_username()))))).update(resolucion=resolucion)
		mensaje="Resolucion guardada correctamente"
		return render(request,'solicitudempresas.html',{'mensaje':mensaje,'cuentas':cuentas})
	if request.POST.get("activar") is not None and existe and resolucion!="":
		rut=request.POST.get("rut")
		user=User.objects.get(username=rut)
		mensaje="La cuenta no pudo activarse"
		if Visita.objects.filter(Empresa=(Empresa.objects.get(Cuenta=cuenta)), Administrador=Administrador.objects.get(Cuenta=Cuenta.objects.get(rut=request.user.get_username()))).exists():
			fec_activacion=datetime.date.today()
			Empresa.objects.filter(Cuenta=cuenta).update(fec_activacion=fec_activacion)
			user.is_active=True
			user.save()
			mensaje="Cuenta activada correctamente"
			return render(request,'solicitudempresas.html',{'mensaje':mensaje,'cuentas':cuentas})

	return render(request,"detalleempresa.html",{'resolucion':resolucion,'existe':existe,'cuenta':cuenta,'mensaje':mensaje, 'visitas':visitas})
