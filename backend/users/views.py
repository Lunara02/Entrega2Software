# backend/users/views.py
from rest_framework import viewsets, permissions
from .models import Usuario
from .serializers import UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]
    # filtrar, listar conductores por ejemplo:
    def get_queryset(self):
        return Usuario.objects.all()
