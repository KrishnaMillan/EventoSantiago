from django import forms


class Login(forms.Form):

	rut=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Sin puntos ni guión'}), label="Rut", required=True)
	contrasena=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': '*******'}), label="Contraseña", required=True)
