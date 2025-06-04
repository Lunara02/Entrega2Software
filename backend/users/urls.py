# backend/users/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'', UsuarioViewSet, basename='usuarios')

urlpatterns = [
    # Endpoints para obtener _todas_ las rutas de UsuarioViewSet
    *router.urls,
    # Endpoints para JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
