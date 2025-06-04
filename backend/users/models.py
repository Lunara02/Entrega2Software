# backend/users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
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
