from django.shortcuts import render
from django.views.generic import(
    ListView, #Recordar borrar las que no se estarán usando
    DetailView,
    CreateView,
    TemplateView,
    UpdateView,
    DeleteView,
    FormView
)

# Create your views here.

class InicioView(TemplateView):
    # vista que carga la pagina de inicio
    template_name="inicio.html"