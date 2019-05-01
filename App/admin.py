from django.contrib import admin
from .models import Cuenta, Usuario, RegistroEmail

admin.site.register(Usuario)
admin.site.register(Cuenta)
admin.site.register(RegistroEmail)

# Register your models here.
