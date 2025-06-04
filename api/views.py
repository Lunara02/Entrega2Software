# api/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Usuario, Estado, Ruta, Paquete, HistorialEstado
from .serializers import (
    UsuarioSerializer,
    EstadoSerializer,
    RutaSerializer,
    PaqueteSerializer, PaqueteCreateSerializer,
    HistorialEstadoSerializer, HistorialEstadoCreateSerializer
)


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Usuarios.
    - Permite crear usuarios (registro) sin autenticación (AllowAny).
    - Resto de acciones requieren token válido (IsAuthenticated).
    - Acción extra 'conductores' lista solo usuarios con tipo_usuario='conductor'.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        # Si la acción es 'create' (registro), permitimos sin autenticación
        if self.action == 'create':
            return [AllowAny()]
        # Para cualquier otra acción, requiere estar autenticado
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        # Al guardar el serializer, el método create de UsuarioSerializer ya hace set_password()
        serializer.save()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def conductores(self, request):
        """
        GET /api/usuarios/conductores/
        Retorna lista de usuarios cuyo tipo_usuario = 'conductor'.
        """
        queryset = Usuario.objects.filter(tipo_usuario='conductor')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class EstadoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de Estados.
    - Solo administradores pueden crear/editar/eliminar estados.
    - Usuarios autenticados pueden listar/recuperar estados.
    """
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class RutaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de Rutas.
    - Solo administradores pueden crear/editar/eliminar rutas.
    - Usuarios autenticados pueden listar/recuperar rutas.
    """
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class PaqueteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de Paquetes.
    - Crear paquete: un cliente autenticado envía { cliente_destinatario, peso, dimensiones }.
      El campo cliente_remitente se asigna automáticamente a request.user.
    - Listar/recuperar: retorna datos anidados de remitente, destinatario, estado y ruta.
    - Acción extra 'cambiar_estado': un conductor puede cambiar el estado del paquete.
    - Acción extra 'historial': lista el historial de estados de un paquete.
    """
    queryset = Paquete.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        # Si estamos en la acción 'create', usamos PaqueteCreateSerializer
        if self.action in ['create']:
            return PaqueteCreateSerializer
        # En cualquier otra (list, retrieve, update…), usamos PaqueteSerializer para lectura
        return PaqueteSerializer

    def perform_create(self, serializer):
        # Asigna automáticamente cliente_remitente = usuario autenticado
        serializer.save(cliente_remitente=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cambiar_estado(self, request, pk=None):
        """
        POST /api/paquetes/{id}/cambiar_estado/
        Cuerpo JSON: { "estado": <id_estado> }
        Solo usuarios con tipo_usuario='conductor' pueden cambiar el estado.
        Al cambiar:
          1) Actualiza Paquete.estado_actual.
          2) Crea un nuevo HistorialEstado con actualizador=request.user.
        """
        paquete = get_object_or_404(Paquete, pk=pk)

        # Verificar que quien hace la petición es un conductor
        if request.user.tipo_usuario != 'conductor':
            return Response(
                {'detail': 'Solo conductores pueden cambiar el estado.'},
                status=status.HTTP_403_FORBIDDEN
            )

        nuevo_estado_id = request.data.get('estado')
        if not nuevo_estado_id:
            return Response(
                {'detail': 'Debe proporcionar el ID del estado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        estado_obj = get_object_or_404(Estado, pk=nuevo_estado_id)
        paquete.estado_actual = estado_obj
        paquete.save()

        HistorialEstado.objects.create(
            paquete=paquete,
            estado=estado_obj,
            actualizador=request.user
        )

        return Response(
            {'detail': f'Estado cambiado a "{estado_obj.nombre}" correctamente.'},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def historial(self, request, pk=None):
        """
        GET /api/paquetes/{id}/historial/
        Devuelve la lista de HistorialEstado para el paquete especificado, ordenada por fecha ascendente.
        """
        paquete = get_object_or_404(Paquete, pk=pk)
        lista_historial = paquete.historiales.all().order_by('fecha')
        serializer = HistorialEstadoSerializer(lista_historial, many=True)
        return Response(serializer.data)


class HistorialEstadoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para HistorialEstado.
    - Solo administradores autenticados pueden ver el historial completo.
    """
    queryset = HistorialEstado.objects.all()
    serializer_class = HistorialEstadoSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
