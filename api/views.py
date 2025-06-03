from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta

from .models import Usuarios, Rutas, Paquetes, Estados, HistorialEstados
from .serializers import (
    UsuarioSerializer,
    RutaSerializer,
    PaqueteSerializer,
    EstadoSerializer,
    HistorialEstadoSerializer
)

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

class PaqueteViewSet(viewsets.ModelViewSet):
    queryset = Paquetes.objects.all()
    serializer_class = PaqueteSerializer
    permission_classes = [AllowAny]

class ConductorViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.filter(tipo_usuario='conductor')
    serializer_class = UsuarioSerializer
    permission_classes = [AllowAny]

class RutaViewSet(viewsets.ModelViewSet):
    queryset = Rutas.objects.all()
    serializer_class = RutaSerializer
    permission_classes = [AllowAny]

class EstadoViewSet(viewsets.ModelViewSet):
    queryset = Estados.objects.all()
    serializer_class = EstadoSerializer
    permission_classes = [IsAuthenticated]

class HistorialEstadoViewSet(viewsets.ModelViewSet):
    queryset = HistorialEstados.objects.all()
    serializer_class = HistorialEstadoSerializer
    permission_classes = [IsAuthenticated]

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    correo = request.data.get('correo')
    contrasena = request.data.get('contrasena')

    try:
        usuario = Usuarios.objects.get(correo=correo)
    except Usuarios.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=404)

    if not check_password(contrasena, usuario.contrasena):
        return Response({'error': 'Contraseña incorrecta'}, status=401)

    refresh = RefreshToken.for_user(usuario)
    access_token = str(refresh.access_token)

    return Response({
        'access': access_token,
        'refresh': str(refresh),
        'usuario': {
            'id': usuario.id,
            'nombre': usuario.nombre,
            'tipo_usuario': usuario.tipo_usuario,
        }
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    refresh_token = request.data.get('refresh')
    
    if not refresh_token:
        return Response({'error': 'Refresh token is required'}, status=400)
    
    try:
        refresh = RefreshToken(refresh_token)
        new_access_token = str(refresh.access_token)
        
        return Response({
            'access': new_access_token
        })
    except Exception as e:
        return Response({'error': str(e)}, status=401)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def registrar_usuario(request):
    data = request.data

    if Usuarios.objects.filter(correo=data['correo']).exists():
        return Response({'error': 'Correo ya registrado'}, status=400)

    try:
        usuario = Usuarios.objects.create(
            nombre=data['nombre'],
            correo=data['correo'],
            contrasena=make_password(data['contrasena']),
            tipo_usuario=data['tipo_usuario']
        )
        return Response({'msg': 'Usuario creado correctamente'}, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=400)