from django.urls import path
from .views import AsignarPaqueteView

urlpatterns = [
    path('asignar/', AsignarPaqueteView.as_view(), name='asignar_paquete'),
]
