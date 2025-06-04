# backend/shipments/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Paquete, HistorialEstado
from .serializers import PaqueteSerializer, HistorialEstadoSerializer
from users.models import Usuario

class PaqueteListCreateView(generics.ListCreateAPIView):
    serializer_class = PaqueteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.tipo_usuario == 'cliente':
            return Paquete.objects.filter(cliente_remitente=user)
        elif user.tipo_usuario == 'conductor':
            return Paquete.objects.filter(ruta__conductor=user)
        return Paquete.objects.none()

    def perform_create(self, serializer):
        serializer.save(cliente_remitente=self.request.user)


class PaqueteDetailView(generics.RetrieveUpdateAPIView):
    queryset = Paquete.objects.all()
    serializer_class = PaqueteSerializer
    permission_classes = [permissions.IsAuthenticated]


class CambiarEstadoView(generics.UpdateAPIView):
    queryset = Paquete.objects.all()
    serializer_class = PaqueteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        paquete = self.get_object()
        nuevo_estado_id = request.data.get('estado_id')
        if not nuevo_estado_id:
            return Response({'detail': 'estado_id obligatorio'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from routes.models import Estado
            estado_obj = Estado.objects.get(id=nuevo_estado_id)
        except Estado.DoesNotExist:
            return Response({'detail': 'Estado no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        # Guardo en HistorialEstado
        HistorialEstado.objects.create(
            paquete=paquete,
            estado=estado_obj,
            actualizador=request.user
        )
        # Actualizo estado_actual del paquete
        paquete.estado_actual = estado_obj
        paquete.save()

        serializer = self.get_serializer(paquete)
        return Response(serializer.data)


class HistorialListView(generics.ListAPIView):
    serializer_class = HistorialEstadoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        paquete_id = self.kwargs['pk']
        return HistorialEstado.objects.filter(paquete_id=paquete_id).order_by('-fecha')
