# backend/project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 1) Administración de Django
    path('admin/', admin.site.urls),

    # 2) Endpoints de autenticación JWT (Simple JWT),
    #    definidos dentro de la app "users"
    path('api/users/token/', include('users.urls')),        # TokenObtainPairView + TokenRefreshView
    #    Si deseas, podrías separar en:
    # path('api/users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair')
    # path('api/users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
    #    pero aquí asumimos que todo está en users/urls.py

    # 3) Rutas de la API “users” (usuarios, listado de conductores/clientes, registro, etc.)
    path('api/users/', include('users.urls')),

    # 4) Rutas de la API “routes” (estados y rutas)
    path('api/routes/', include('routes.urls')),

    # 5) Rutas de la API “shipments” (paquetes e historial)
    path('api/shipments/', include('shipments.urls')),

    # 6) Rutas de la API “maps” (futura integración con mapas/geo)
    path('api/maps/', include('maps.urls')),

    # 7) Vistas web (“frontend”): index y panel
    path('', include('frontend.urls')),
]
