# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    UsuarioViewSet,
    EstadoViewSet,
    RutaViewSet,
    PaqueteViewSet,
    HistorialEstadoViewSet
)

# Creamos el router y registramos los ViewSets
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')
router.register(r'estados', EstadoViewSet, basename='estados')
router.register(r'rutas', RutaViewSet, basename='rutas')
router.register(r'paquetes', PaqueteViewSet, basename='paquetes')
router.register(r'historial', HistorialEstadoViewSet, basename='historial')

urlpatterns = [
    # Endpoints para obtener/renovar tokens JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Incluir todas las rutas generadas por el router
    path('', include(router.urls)),
]
