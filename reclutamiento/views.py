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
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator    

# Create your views here.

class InicioView(TemplateView):
    # vista que carga la pagina de inicio
    template_name="inicio.html"

from django.shortcuts import render, redirect
from .forms import VacanteForm

def crear_vacante(request):
    if request.method == 'POST':
        form = VacanteForm(request.POST)
        if form.is_valid():
            form.save() # Recordar que aquí guardamos en las BD
            return redirect('reclutamiento_app:plantilla_admin')
        else:
            print("Error de form")
            print(form.errors)
    else:
        # Si el método es GET, se muestra un formulario vacío
        form = VacanteForm()
    
    # Se renderiza la plantilla con el contexto del formulario
    return render(request, 'admin/crear_vacantes.html', {'form': form})

from .models import *

# reclutamiento_app/views.py

from django.views.generic import ListView
from .models import Vacante

@method_decorator(staff_member_required, name='dispatch')
class DashboardView(ListView):
    
    model = Vacante
    
    template_name = 'admin/dashboard.html'

    context_object_name = 'vacantes_recientes'
    print("Se entra a la función")
    
    def get_queryset(self):
        """Devuelve las últimas 5 vacantes publicadas."""
        return Vacante.objects.all()[:5]
    
@method_decorator(staff_member_required, name='dispatch')
class ListaVacantes(TemplateView):
    template_name="admin/vacantes_lista.html"
