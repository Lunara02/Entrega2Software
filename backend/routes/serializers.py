# backend/routes/serializers.py
from rest_framework import serializers
from .models import Estado, Ruta
from users.serializers import UsuarioSerializer

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = ['id', 'nombre']


class RutaSerializer(serializers.ModelSerializer):
    conductor = UsuarioSerializer(read_only=True)
    conductor_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Ruta
        fields = ['id', 'origen', 'destino', 'distancia_km', 'duracion_estimada', 'conductor', 'conductor_id']
