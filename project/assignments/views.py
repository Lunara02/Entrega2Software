from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from packages.models import Paquete
from django.contrib.auth import get_user_model

User = get_user_model()

class AsignarPaqueteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        paquete_id = request.data.get('paquete_id')
        conductor_id = request.data.get('conductor_id')

        if not paquete_id or not conductor_id:
            return Response({"error": "Faltan datos"}, status=400)

        # Validar que quien asigna tenga permisos de administrador
        if request.user.rol != 'admin':
            return Response({"error": "No tienes permisos para asignar paquetes"}, status=403)

        try:
            paquete = Paquete.objects.get(id=paquete_id)
            conductor = User.objects.get(id=conductor_id, rol='conductor')
        except Paquete.DoesNotExist:
            return Response({"error": "Paquete no encontrado"}, status=404)
        except User.DoesNotExist:
            return Response({"error": "Conductor no válido"}, status=404)

        paquete.conductor = conductor
        paquete.save()

        return Response({
            "message": "Paquete asignado exitosamente",
            "paquete": paquete.id,
            "conductor": conductor.username
        })
