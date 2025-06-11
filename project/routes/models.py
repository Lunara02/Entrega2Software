from django.db import models


class Ruta(models.Model):
    origen = models.CharField(max_length=255)
    destinos = models.TextField()
    distancia_total = models.FloatField()
    duracion_total = models.FloatField()
    creada_en = models.DateTimeField(auto_now_add=True)


class Sede(models.Model):
    direccion = models.CharField(max_length=255)
    latitud = models.FloatField()
    longitud = models.FloatField()
    actualizada_en = models.DateTimeField(auto_now=True)
