# backend/routes/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import EstadoViewSet, RutaViewSet

router = DefaultRouter()
router.register(r'estados', EstadoViewSet, basename='estados')
router.register(r'rutas', RutaViewSet, basename='rutas')

urlpatterns = router.urls
