# backend/shipments/urls.py
from django.urls import path
from .views import (
    PaqueteListCreateView,
    PaqueteDetailView,
    CambiarEstadoView,
    HistorialListView,
)

urlpatterns = [
    path('', PaqueteListCreateView.as_view(), name='paquetes-list-create'),
    path('<int:pk>/', PaqueteDetailView.as_view(), name='paquetes-detail'),
    path('<int:pk>/cambiar_estado/', CambiarEstadoView.as_view(), name='paquetes-cambiar-estado'),
    path('<int:pk>/historial/', HistorialListView.as_view(), name='paquetes-historial'),
]
