from django import forms

class AgregaUsuario(forms.Form):
	nombre=forms.CharField(widget=forms.TextInput(), label="Nombre")
	rut=forms.CharField(widget=forms.TextInput(), label="Rut")
	fec_nac=forms.DateField(widget=forms.DateInput(),label="Fecha de Nacimiento")
	correoAsociado=forms.CharField(widget=forms.TextInput(), label="Correo")
	contrasena=forms.CharField(widget=forms.PasswordInput(), label="Contraseña")

class Login(forms.Form):
	rut=forms.CharField(widget=forms.TextInput(), label="Rut")
	contrasena=forms.CharField(widget=forms.PasswordInput(), label="Contraseña")