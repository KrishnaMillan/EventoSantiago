from django.db import models

# Create your models here.
class Cuenta(models.Model):
	id_cuenta=models.CharField(max_length=15, primary_key=True)
	nombre=models.CharField(max_length=1000)
	rut=models.CharField(max_length=15)
	correoAsociado=models.TextField()
	#contrasena= Verificar en user. onetoofield
	tipo_usuario=models.CharField(max_length=5)
	def __str__(self):
		 return self.nombre + " "

class Usuario(Cuenta):
	fec_nac=models.DateField(max_length=15)
	esactiva=models.BooleanField(default=True)





