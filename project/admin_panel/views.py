from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrSecretario
from django.contrib.auth import get_user_model
from packages.models import Paquete
from rest_framework import status

User = get_user_model()


def es_admin(usuario):
    return usuario.rol == 'admin'



class ListaUsuariosView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSecretario]

    def get(self, request):

        usuarios = User.objects.all()
        data = []

        for u in usuarios:
            data.append({
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "rol": u.rol,
                "activo": u.is_active
            })

        return Response(data, status=200)


class ListaConductoresView(APIView):
    """Retorna todos los usuarios con rol de conductor."""
    permission_classes = [IsAuthenticated, IsAdminOrSecretario]

    def get(self, request):
        conductores = User.objects.filter(rol='conductor')
        data = []
        for c in conductores:
            data.append({
                "id": c.id,
                "username": c.username,
                "email": c.email,
            })
        return Response(data, status=200)


class ListaPaquetesAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSecretario]

    def get(self, request):
        estado = request.query_params.get('estado')
        paquetes = Paquete.objects.all()
        if estado:
            paquetes = paquetes.filter(estado=estado)

        data = []
        for p in paquetes:
            data.append({
                "id": p.id,
                "cliente": p.cliente.username,
                "conductor": p.conductor.username if p.conductor else None,
                "estado": p.estado,
                "direccion_destino": p.direccion_destino,
                "fecha_creacion": p.fecha_creacion
            })

        return Response(data)


class EstadisticasGeneralesView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSecretario]

    def get(self, request):
        total_usuarios = User.objects.count()
        total_paquetes = Paquete.objects.count()
        entregados = Paquete.objects.filter(estado='entregado').count()
        en_ruta = Paquete.objects.filter(estado='en_ruta').count()
        pendientes = Paquete.objects.filter(estado='pendiente').count()

        return Response({
            "usuarios_total": total_usuarios,
            "paquetes_total": total_paquetes,
            "paquetes_entregados": entregados,
            "paquetes_en_ruta": en_ruta,
            "paquetes_pendientes": pendientes
        })
