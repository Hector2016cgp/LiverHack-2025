from django.urls import path
from .views import DashboardCandidatoView, ActualizarPerfilView, MisPostulacionesView, VacantesDisponiblesView

app_name = "Candidatos"  

urlpatterns = [
    path('dashboard/', DashboardCandidatoView.as_view(), name='dashboard_candidato'),
    path('perfil/editar/', ActualizarPerfilView.as_view(), name='actualizar_perfil'),
    path('mis-postulaciones/', MisPostulacionesView.as_view(), name='mis_postulaciones'),
    path('vacantes-disponibles/', VacantesDisponiblesView.as_view(), name='vacantes_disponibles'),
]