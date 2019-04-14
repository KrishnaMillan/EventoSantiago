from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.
def index(request):

#INICIO
   # personas=Persona.objects.all()
    #mascotas=Mascota.objects.all()
    plantilla=loader.get_template("index.html")
    contexto={}
     #   'mascotas':mascotas,
     #   'personas':personas
    #}
    return HttpResponse(plantilla.render(contexto,request))
