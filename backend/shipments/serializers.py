# backend/shipments/serializers.py
from rest_framework import serializers
from .models import Paquete, HistorialEstado
from users.serializers import UsuarioSerializer
from routes.serializers import EstadoSerializer

class PaqueteSerializer(serializers.ModelSerializer):
    cliente_remitente = UsuarioSerializer(read_only=True)
    cliente_destinatario_id = serializers.IntegerField(write_only=True)
    estado_actual = EstadoSerializer(read_only=True)

    class Meta:
        model = Paquete
        fields = ['id', 'cliente_remitente', 'cliente_destinatario_id', 'peso', 'dimensiones', 'estado_actual', 'ruta', 'fecha_envio']
        read_only_fields = ['cliente_remitente', 'fecha_envio', 'estado_actual']


class HistorialEstadoSerializer(serializers.ModelSerializer):
    estado = EstadoSerializer(read_only=True)
    actualizador = UsuarioSerializer(read_only=True)

    class Meta:
        model = HistorialEstado
        fields = ['id', 'paquete', 'estado', 'fecha', 'actualizador']
