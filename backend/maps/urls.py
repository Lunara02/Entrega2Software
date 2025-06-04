# backend/maps/urls.py
from django.urls import path
from .views import CalculaRutaAPIView  # definirla más abajo

urlpatterns = [
    # Aquí irán endpoints como:
    # path('distance/', CalculaRutaAPIView.as_view(), name='maps-distance'),
]
