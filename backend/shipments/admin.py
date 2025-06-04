# backend/shipments/admin.py
from django.contrib import admin
from .models import Paquete, HistorialEstado

@admin.register(Paquete)
class PaqueteAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente_remitente', 'cliente_destinatario', 'estado_actual', 'ruta', 'fecha_envio']

@admin.register(HistorialEstado)
class HistorialEstadoAdmin(admin.ModelAdmin):
    list_display = ['id', 'paquete', 'estado', 'actualizador', 'fecha']
