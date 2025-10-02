from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static  


app_name = "reclutamiento_app"

urlpatterns = [
    path('', views.InicioView.as_view(), name='Inicio'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)