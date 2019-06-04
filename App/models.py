from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Cuenta(models.Model):
	rut=models.CharField(max_length=15, primary_key=True)
	nombre=models.CharField(max_length=1000, null=True)
	correoAsociado=models.TextField(null=True)
	#tipo_usuario=models.CharField(max_length=5, choices=tiposUsuarios, null=True)
	#esactiva=models.BooleanField(default=True, null=True)
	user=models.OneToOneField(User,on_delete=models.CASCADE, null=True )
	fecha_registro=models.DateField(max_length=15, null=True)
	comuna=models.CharField(max_length=1000, null=True)

class Usuario(models.Model):
	Cuenta=models.ForeignKey(Cuenta, on_delete=models.CASCADE)
	fec_nac=models.DateField(max_length=15, null=True)

class RegistroEmail(models.Model):
	Cuenta=models.ForeignKey(Cuenta, on_delete=models.CASCADE, null=True)
	iduuid=models.CharField(max_length=1000, null=True)

class Administrador(models.Model):
	Cuenta=models.ForeignKey(Cuenta, on_delete=models.CASCADE, null=True)
	fec_nac=models.DateField(max_length=15)
	fec_ingreso=models.DateField(max_length=15)

class Empresa(models.Model):
	Cuenta=models.ForeignKey(Cuenta, on_delete=models.CASCADE, null=True)
	fec_activacion=models.DateField(max_length=15, null=True)
	direccion=models.CharField(max_length=150)

class Evento(models.Model):
	id_evento=models.AutoField(max_length=15,primary_key=True)
	nombre=models.CharField(max_length=1500)
	descripcion=models.CharField(max_length=1000000000, null=True)
	fecha=models.DateField(max_length=15)
	hora=models.TimeField(max_length=15)
	comuna=models.CharField(max_length=15)
	direccion=models.CharField(max_length=150)
	cant_cupos=models.CharField(max_length=15)
	pagReserva=models.CharField(max_length=100000000000,null=True)
	estado=models.BooleanField(default=True)
	Empresa=models.ForeignKey(Empresa, on_delete=models.CASCADE)

class Reserva(models.Model):
	id_reserva=models.AutoField(max_length=15,primary_key=True)
	fecha=models.DateField(max_length=15)
	hora=models.TimeField(max_length=15)
	Evento=models.ForeignKey(Evento, on_delete=models.CASCADE)
	Usuario=models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Visita(models.Model):
	id_visita=models.AutoField(primary_key=True)
	fecha_visita=models.DateField(max_length=15)
	resolucion=models.CharField(max_length=5000, null=True)
	Empresa=models.ForeignKey(Empresa, on_delete=models.CASCADE)
	Administrador=models.ForeignKey(Administrador, on_delete=models.CASCADE)
