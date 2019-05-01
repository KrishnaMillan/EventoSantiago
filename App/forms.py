from django import forms


class Login(forms.Form):
	rut=forms.CharField(widget=forms.TextInput(), label="Rut", required=True)
	contrasena=forms.CharField(widget=forms.PasswordInput(), label="Contraseña", required=True)
