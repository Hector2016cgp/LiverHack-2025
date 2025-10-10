# candidato/views.py
from django.views.generic import TemplateView, DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from reclutamiento.models import Vacante
from .models import Candidato, Postulacion
from .forms import PerfilCandidatoForm 

class DashboardCandidatoView(LoginRequiredMixin, TemplateView):
    template_name = 'candidatos/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        candidato, created = Candidato.objects.get_or_create(user=self.request.user)
        
        context['candidato'] = candidato
        context['postulaciones'] = Postulacion.objects.filter(candidato=candidato).order_by('-fecha_postulacion')
        context['perfil_form'] = PerfilCandidatoForm(instance=candidato)
        
        from django.utils import timezone
        hoy = timezone.now().date()
        context['vacantes_disponibles'] = Vacante.objects.filter(fecha_cierre__gte=hoy)
        
        return context


class ActualizarPerfilView(LoginRequiredMixin, UpdateView):
    """
    Vista para actualizar el perfil del candidato.
    """
    model = Candidato
    form_class = PerfilCandidatoForm
    template_name = 'candidatos/dashboard.html'
    success_url = reverse_lazy('Candidatos:dashboard_candidato')  # Usa el namespace

    def get_object(self, queryset=None):
        return self.request.user.candidato

    def form_valid(self, form):
        messages.success(self.request, '¡Tu perfil se ha actualizado correctamente!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corrige los errores en el formulario.')
        # Aquí hay un error en tu código original, debería ser:
        return self.render_to_response(self.get_context_data(form=form))


class MisPostulacionesView(LoginRequiredMixin, ListView):
    """
    Lista todas las postulaciones del candidato.
    """
    model = Postulacion
    template_name = 'candidatos/mis_postulaciones.html'  # Corregí la ruta
    context_object_name = 'postulaciones'

    def get_queryset(self):
        return Postulacion.objects.filter(candidato=self.request.user.candidato).order_by('-fecha_postulacion')


class VacantesDisponiblesView(LoginRequiredMixin, ListView):
    """
    Lista las vacantes activas disponibles para postular.
    """
    model = Vacante
    template_name = 'candidatos/vacantes_lista.html' 
    context_object_name = 'vacantes'

    def get_queryset(self):
        from django.utils import timezone
        hoy = timezone.now().date()
        return Vacante.objects.filter(fecha_cierre__gte=hoy).order_by('fecha_cierre')