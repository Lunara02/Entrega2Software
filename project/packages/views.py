from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Paquete
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
User = get_user_model()


class CrearPaqueteView(APIView):
    def post(self, request):
        cliente_id = request.data.get('cliente_id')
        direccion = request.data.get('direccion_destino')
        lat = request.data.get('lat')
        lon = request.data.get('lon')

        if not cliente_id or not direccion or lat is None or lon is None:
            return Response({"error": "Faltan datos"}, status=400)

        try:
            cliente = User.objects.get(id=cliente_id)
        except User.DoesNotExist:
            return Response({"error": "Cliente no encontrado"}, status=404)

        paquete = Paquete.objects.create(
            cliente=cliente,
            direccion_destino=direccion,
            latitud=lat,
            longitud=lon
        )

        return Response({
            "message": "Paquete creado",
            "paquete": {
                "id": paquete.id,
                "cliente": cliente.username,
                "direccion_destino": paquete.direccion_destino,
                "latitud": paquete.latitud,
                "longitud": paquete.longitud,
                "estado": paquete.estado,
                "fecha_creacion": paquete.fecha_creacion,
            }
        }, status=201)


class ListaPaquetesView(APIView):
    def get(self, request):
        paquetes = Paquete.objects.all().order_by('-fecha_creacion')
        datos = []

        for p in paquetes:
            datos.append({
                "id": p.id,
                "cliente": p.cliente.username,
                "direccion_destino": p.direccion_destino,
                "latitud": p.latitud,
                "longitud": p.longitud,
                "estado": p.estado,
                "fecha_creacion": p.fecha_creacion
            })

        return Response(datos)
    
class ActualizarEstadoPaqueteView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, paquete_id):
        nuevo_estado = request.data.get('estado')

        if not nuevo_estado:
            return Response({"error": "Falta el campo 'estado'"}, status=400)

        try:
            paquete = Paquete.objects.get(id=paquete_id)
        except Paquete.DoesNotExist:
            return Response({"error": "Paquete no encontrado"}, status=404)

        # Verificar que el usuario actual es el conductor asignado
        if paquete.conductor != request.user:
            return Response({"error": "No tienes permiso para modificar este paquete"}, status=403)

        paquete.estado = nuevo_estado
        paquete.save()

        return Response({
            "message": "Estado actualizado",
            "paquete": {
                "id": paquete.id,
                "estado": paquete.estado
            }
        }, status=200)
    
class PaquetesDelConductorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.rol != 'conductor':
            return Response({"error": "Solo conductores pueden acceder a este endpoint"}, status=403)

        paquetes = Paquete.objects.filter(conductor=request.user)
        datos = []

        for p in paquetes:
            datos.append({
                "id": p.id,
                "cliente": p.cliente.username,
                "direccion_destino": p.direccion_destino,
                "latitud": p.latitud,
                "longitud": p.longitud,
                "estado": p.estado,
                "fecha_creacion": p.fecha_creacion
            })

        return Response(datos, status=200)
    


class PedidosDelClienteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.rol != 'cliente':
            return Response({"error": "Solo los clientes pueden ver sus pedidos"}, status=403)

        paquetes = Paquete.objects.filter(cliente=request.user).order_by('-fecha_creacion')
        datos = []

        for p in paquetes:
            datos.append({
                "id": p.id,
                "direccion_destino": p.direccion_destino,
                "latitud": p.latitud,
                "longitud": p.longitud,
                "estado": p.estado,
                "fecha_creacion": p.fecha_creacion,
                "conductor": p.conductor.username if p.conductor else None
            })

        return Response(datos, status=200)
