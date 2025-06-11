from django.urls import path
from .views import CrearRutaView, SedeView

urlpatterns = [
    path('crear/', CrearRutaView.as_view(), name='crear_ruta'),
    path('sede/', SedeView.as_view(), name='sede'),
]
