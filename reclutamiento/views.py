from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, CreateView
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .forms import VacanteForm, AdminAuthenticationForm, RegistroForm
from .models import Vacante

# ================================
# VISTAS GENERALES
# ================================

class InicioView(TemplateView):
    template_name = "inicio.html"

# ================================
# VISTAS DE VACANTES
# ================================

def crear_vacante(request):
    if request.method == 'POST':
        form = VacanteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reclutamiento_app:plantilla_admin')
    else:
        form = VacanteForm()
    return render(request, 'admin/crear_vacantes.html', {'form': form})

@method_decorator(staff_member_required, name='dispatch')
class DashboardView(ListView):
    model = Vacante
    template_name = 'admin/dashboard.html'
    context_object_name = 'vacantes_recientes'

    def get_queryset(self):
        return Vacante.objects.all()[:5]

@method_decorator(staff_member_required, name='dispatch')
class ListaVacantes(ListView):
    model = Vacante
    template_name = "admin/vacantes_lista.html"
    context_object_name = "vacantes"

    def get_queryset(self):
        query = self.request.GET.get("search")
        qs = Vacante.objects.all()
        if query:
            qs = qs.filter(titulo__icontains=query)
        return qs

# ================================
# VISTAS DE AUTENTICACIÓN
# ================================
class RegistroView(CreateView):
    model = User
    form_class = RegistroForm 
    template_name = 'registration/register.html'
    success_url = reverse_lazy('reclutamiento_app:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        
        from candidatos.models import Candidato
        Candidato.objects.get_or_create(user=self.object)
        
        return response

class LoginView(DjangoLoginView):
    template_name = "registration/login.html"

    def get_success_url(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return reverse_lazy('reclutamiento_app:plantilla_admin')
        return reverse_lazy('Candidatos:dashboard_candidato')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy('Inicio')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

def login_redirect_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('reclutamiento_app:plantilla_admin')
        else:
            return redirect('Candidatos:dashboard_candidato')
    return redirect('reclutamiento_app:Inicio')
