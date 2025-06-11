from django.urls import path
from .views import CrearPaqueteView, ListaPaquetesView
from .views import ActualizarEstadoPaqueteView
from .views import PaquetesDelConductorView
from .views import PedidosDelClienteView

urlpatterns = [
    path('crear/', CrearPaqueteView.as_view(), name='crear_paquete'),
    path('listar/', ListaPaquetesView.as_view(), name='listar_paquetes'),
    path('<int:paquete_id>/estado/', ActualizarEstadoPaqueteView.as_view(), name='actualizar_estado'),
    path('mis-paquetes/', PaquetesDelConductorView.as_view(), name='mis_paquetes'),
    path('mis-pedidos/', PedidosDelClienteView.as_view(), name='mis_pedidos'),
]
