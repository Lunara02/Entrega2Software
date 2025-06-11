from django.urls import path
from .views import (
    ListaUsuariosView,
    ListaPaquetesAdminView,
    EstadisticasGeneralesView,
    ListaConductoresView,
)

urlpatterns = [
    path('usuarios/', ListaUsuariosView.as_view(), name='admin_usuarios'),
    path('conductores/', ListaConductoresView.as_view(), name='admin_conductores'),
    path('paquetes/', ListaPaquetesAdminView.as_view(), name='admin_paquetes'),
    path('estadisticas/', EstadisticasGeneralesView.as_view(), name='admin_estadisticas'),
]
