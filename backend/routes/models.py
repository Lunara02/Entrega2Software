# backend/routes/models.py
from django.db import models
from users.models import Usuario  # importamos el modelo Usuario para la FK

class Estado(models.Model):
    nombre = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'estados'
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'


class Ruta(models.Model):
    origen = models.TextField()
    destino = models.TextField()
    distancia_km = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    duracion_estimada = models.IntegerField(blank=True, null=True, help_text="Duración en minutos")
    conductor = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='rutas'
    )

    def __str__(self):
        return f"{self.origen} → {self.destino}"

    class Meta:
        db_table = 'rutas'
        verbose_name = 'Ruta'
        verbose_name_plural = 'Rutas'
