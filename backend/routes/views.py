# backend/routes/views.py
from rest_framework import viewsets, permissions
from .models import Estado, Ruta
from .serializers import EstadoSerializer, RutaSerializer

class EstadoViewSet(viewsets.ModelViewSet):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer
    permission_classes = [permissions.IsAdminUser]  # solo admins pueden crear/editar estados


class RutaViewSet(viewsets.ModelViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer
    permission_classes = [permissions.IsAdminUser]  # solo admins pueden crear/editar rutas
