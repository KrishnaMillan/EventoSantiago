from django.db import models

# Create your models here.

class Cuenta(models.Model):
	id_cuenta=models.CharField(max_length=15, primary_key=True)
	nombre=models.CharField(max_length=1000)
	rut=models.CharField(max_length=15)
	correoAsociado=models.TextField()
	#contrasena= Verificar en user. onetoofield
	tipo_usuario=models.CharField(max_length=5)
	esactiva=models.BooleanField(default=True)
	fecha_registro=models.DateField(max_length=15, null=True)

class Usuario(Cuenta):
	fec_nac=models.DateField(max_length=15)
	
class Administrador(Cuenta):
	fec_nac=models.DateField(max_length=15)
	fec_ingreso=models.DateField(max_length=15)

class Empresa(Cuenta):
	fec_activacion=models.DateField(max_length=15)

class Evento(models.Model):
	id_evento=models.CharField(max_length=15,primary_key=True)
	fecha=models.DateField(max_length=15)
	hora=models.DateTimeField(max_length=15)
	comuna=models.CharField(max_length=15)
	direccion=models.CharField(max_length=15)
	cant_cupos=models.CharField(max_length=15)
	pagReserva=models.BooleanField(default=True)
	Empresa=models.ForeignKey(Empresa, on_delete=models.CASCADE)
class Reserva(models.Model):
	id_reserva=models.CharField(max_length=15,primary_key=True)
	fecha=models.DateField(max_length=15)
	hora=models.DateTimeField(max_length=15)
	Evento=models.ForeignKey(Evento, on_delete=models.CASCADE)
	Usuario=models.ForeignKey(Usuario, on_delete=models.CASCADE)
class TipoUsuario(models.Model):
	id_tipo=models.CharField(max_length=15,primary_key=True)
	descripcion=models.CharField(max_length=15)

class Visita(models.Model):
	id_visita=models.CharField(max_length=15,primary_key=True)
	fecha_visita=models.DateField(max_length=15)
	resolucion=models.CharField(max_length=5000)
	Empresa=models.ForeignKey(Empresa, on_delete=models.CASCADE)
	Administrador=models.ForeignKey(Administrador, on_delete=models.CASCADE)