from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static  


app_name = "reclutamiento_app"

urlpatterns = [
    path('', views.InicioView.as_view(), name='Inicio'),
    path('reclutador/', views.DashboardView.as_view(), name='plantilla_admin'),
    path('nueva/', views.crear_vacante, name='crear_vacante'),
    path('vacantes/', views.ListaVacantes.as_view(), name='lista_vacantes')    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   