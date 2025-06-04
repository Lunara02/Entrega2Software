# api/serializers.py

from rest_framework import serializers
from .models import Usuario, Estado, Ruta, Paquete, HistorialEstado

#
# 1) Serializer para Usuario (registro y detalle)
#
class UsuarioSerializer(serializers.ModelSerializer):
    # password solo se escribe al crear, no se devuelve en las respuestas
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ('id', 'username', 'email', 'tipo_usuario', 'password')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario

#
# 2) Serializer para Estado
#
class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = ('id', 'nombre')

#
# 3) Serializer para Ruta
#
class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = ('id', 'origen', 'destino', 'distancia_km', 'duracion_estimada', 'conductor')

#
# 4) Serializer para Paquete (lectura y creación)
#

class PaqueteSerializer(serializers.ModelSerializer):
    cliente_remitente = UsuarioSerializer(read_only=True)
    cliente_destinatario = UsuarioSerializer(read_only=True)
    estado_actual = EstadoSerializer(read_only=True)
    ruta = RutaSerializer(read_only=True)

    class Meta:
        model = Paquete
        fields = (
            'id',
            'cliente_remitente',
            'cliente_destinatario',
            'ruta',
            'estado_actual',
            'peso',
            'dimensiones',
            'fecha_envio'
        )

class PaqueteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paquete
        fields = ('cliente_destinatario', 'peso', 'dimensiones')
        # No incluimos cliente_remitente; lo asignamos en la vista desde request.user

#
# 5) Serializer para HistorialEstado (lectura y creación)
#

class HistorialEstadoSerializer(serializers.ModelSerializer):
    estado = EstadoSerializer(read_only=True)
    paquete = PaqueteSerializer(read_only=True)
    actualizador = UsuarioSerializer(read_only=True)

    class Meta:
        model = HistorialEstado
        fields = ('id', 'paquete', 'estado', 'fecha', 'actualizador')

class HistorialEstadoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialEstado
        fields = ('paquete', 'estado', 'actualizador')
