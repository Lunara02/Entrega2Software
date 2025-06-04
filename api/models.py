# api/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    """
    Hereda de AbstractUser para usar el sistema de autenticación de Django.
    username, password, email, etc. ya están incluidos.
    """
    TIPO_USUARIO = [
        ('cliente', 'Cliente'),
        ('conductor', 'Conductor'),
        ('admin', 'Administrador'),
    ]
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO, default='cliente')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.tipo_usuario})"

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

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
