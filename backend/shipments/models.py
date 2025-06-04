# backend/shipments/models.py
from django.db import models
from users.models import Usuario
from routes.models import Ruta, Estado

class Paquete(models.Model):
    cliente_remitente = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='envios_realizados'
    )
    cliente_destinatario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='envios_recibidos'
    )
    ruta = models.ForeignKey(Ruta, on_delete=models.SET_NULL, null=True, blank=True)
    estado_actual = models.ForeignKey(Estado, on_delete=models.SET_NULL, null=True, blank=True)
    peso = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    dimensiones = models.TextField(blank=True, null=True)
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Paquete {self.id} – {self.cliente_remitente.username} → {self.cliente_destinatario.username}"

    class Meta:
        db_table = 'paquetes'
        verbose_name = 'Paquete'
        verbose_name_plural = 'Paquetes'


class HistorialEstado(models.Model):
    paquete = models.ForeignKey(
        Paquete,
        on_delete=models.CASCADE,
        related_name='historiales'
    )
    estado = models.ForeignKey(Estado, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    actualizador = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Usuario que cambió el estado"
    )

    def __str__(self):
        nombre_estado = self.estado.nombre if self.estado else 'Desconocido'
        return f"{self.paquete.id} → {nombre_estado} a las {self.fecha}"

    class Meta:
        db_table = 'historial_estados'
        verbose_name = 'Historial de Estado'
        verbose_name_plural = 'Historial de Estados'
