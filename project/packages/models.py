from django.db import models
from django.conf import settings


class Paquete(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('en_ruta', 'En Ruta'),
        ('entregado', 'Entregado'),
    )

    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='paquetes'
    )
    conductor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='paquetes_asignados'
    )
    direccion_destino = models.CharField(max_length=255)
    latitud = models.FloatField()
    longitud = models.FloatField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Paquete #{self.id} - {self.estado}"
