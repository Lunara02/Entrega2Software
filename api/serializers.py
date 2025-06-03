from rest_framework import serializers
from .models import Usuarios, Rutas, Paquetes, Estados, HistorialEstados
from django.contrib.auth.hashers import make_password

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = '__all__'

    def create(self, validated_data):
        validated_data['contrasena'] = make_password(validated_data['contrasena'])
        return super().create(validated_data)

class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rutas
        fields = '__all__'

class PaqueteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paquetes
        fields = '__all__'

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estados
        fields = '__all__'

class HistorialEstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialEstados
        fields = '__all__'
