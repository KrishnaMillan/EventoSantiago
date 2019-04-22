from django import forms

class AgregaUsuario(forms.Form):
	nombre=forms.CharField(widget=forms.TextInput(), label="Nombre")
	rut=forms.CharField(widget=forms.TextInput(), label="Rut")
	fec_nac=forms.DateField(widget=forms.DateInput(),label="Fecha de Nacimiento")
	correoAsociado=forms.CharField(widget=forms.TextInput(), label="Correo")
	comuna=forms.CharField(widget=forms.TextInput(), label="Comuna")
	contrasena=forms.CharField(widget=forms.PasswordInput(), label="Contraseña")
	contrasena2=forms.CharField(widget=forms.PasswordInput(), label="Repetir Contraseña")

class Login(forms.Form):
	rut=forms.CharField(widget=forms.TextInput(), label="Rut")
	contrasena=forms.CharField(widget=forms.PasswordInput(), label="Contraseña")

class ActualizaUsuario(forms.Form):
	nombre=forms.CharField(widget=forms.TextInput(), label="Nombre", required=False)
	fec_nac=forms.DateField(widget=forms.DateInput(),label="Fecha de Nacimiento", required=False)
	comuna=forms.CharField(widget=forms.TextInput(), label="Comuna", required=False)
	correoAsociado=forms.CharField(widget=forms.TextInput(), label="Correo", required=False)

class RecuperaContrasena(forms.Form):
	rut=forms.CharField(widget=forms.TextInput(), label="Rut")

class RecuperaContrasena2(forms.Form):	
	contrasena=forms.CharField(widget=forms.PasswordInput(), label="Contraseña")
	contrasena2=forms.CharField(widget=forms.PasswordInput(), label="Repetir Contraseña")