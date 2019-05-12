from django.contrib import admin
from .models import Cuenta, Usuario, RegistroEmail, Empresa, Administrador, Evento, Reserva, Visita

admin.site.register(Usuario)
admin.site.register(Cuenta)
admin.site.register(RegistroEmail)
admin.site.register(Empresa)
admin.site.register(Administrador)
admin.site.register(Evento)
admin.site.register(Reserva)
admin.site.register(Visita)

# Register your models here.
