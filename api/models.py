from django.db import models

class Estados(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'estados'


class Usuarios(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.CharField(unique=True, max_length=100)
    contrasena = models.CharField(max_length=100)
    tipo_usuario = models.CharField(max_length=20)
    fecha_registro = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.tipo_usuario})"

    class Meta:
        managed = False
        db_table = 'usuarios'


class Rutas(models.Model):
    id = models.AutoField(primary_key=True)
    origen = models.TextField()
    destino = models.TextField()
    distancia_km = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    duracion_estimada = models.IntegerField(blank=True, null=True)
    conductor = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True, blank=True, related_name='rutas')

    def __str__(self):
        return f"{self.origen} → {self.destino}"

    class Meta:
        managed = False
        db_table = 'rutas'


class Paquetes(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Usuarios, on_delete=models.CASCADE, null=True, blank=True, related_name='paquetes')
    ruta = models.ForeignKey(Rutas, on_delete=models.SET_NULL, null=True, blank=True)
    estado_actual = models.ForeignKey(Estados, on_delete=models.SET_NULL, null=True, blank=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    dimensiones = models.TextField(blank=True, null=True)
    fecha_envio = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Paquete {self.id} - Cliente: {self.cliente}"

    class Meta:
        managed = False
        db_table = 'paquetes'


class HistorialEstados(models.Model):
    id = models.AutoField(primary_key=True)
    paquete = models.ForeignKey(Paquetes, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.ForeignKey(Estados, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.paquete} - {self.estado} @ {self.fecha}"

    class Meta:
        managed = False
        db_table = 'historial_estados'
