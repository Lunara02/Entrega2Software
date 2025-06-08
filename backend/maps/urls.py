from django.urls import path
from .views import CalculaRutaAPIView  # definirla más abajo

urlpatterns = [
    path('calcula_ruta/', CalculaRutaAPIView.as_view(), name='calcula_ruta'),
    # Aquí puedes añadir más URLs relacionadas con mapas

]
