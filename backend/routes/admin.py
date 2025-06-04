# backend/routes/admin.py
from django.contrib import admin
from .models import Estado, Ruta

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']

@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ['id', 'origen', 'destino', 'conductor']
