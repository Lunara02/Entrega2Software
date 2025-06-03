from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PaqueteViewSet,
    ConductorViewSet,
    RutaViewSet,
    EstadoViewSet,
    HistorialEstadoViewSet,
    login,
    refresh_token,
    registrar_usuario
)

router = DefaultRouter()
router.register(r'paquetes', PaqueteViewSet)
router.register(r'conductores', ConductorViewSet)
router.register(r'rutas', RutaViewSet)
router.register(r'estados', EstadoViewSet)
router.register(r'historial', HistorialEstadoViewSet)

urlpatterns = [
    path('login/', login, name='login'),
    path('registrar/', registrar_usuario, name='registrar'),
    path('token/refresh/', refresh_token, name='token_refresh'),
    path('', include(router.urls)),
]
