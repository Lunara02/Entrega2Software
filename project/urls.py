from django.contrib import admin
from django.urls import path, include
from api.views_frontend import vista_index, vista_panel

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # API REST (todas las rutas registradas en api/urls.py)
    path('api/', include('api.urls')),

    # Vistas Front-end
    path('', vista_index, name='home'),         # http://localhost:8000/ → carga project/templates/api/index.html
    path('panel/', vista_panel, name='panel'),  # http://localhost:8000/panel/ → carga project/templates/api/panel.html (requiere login)
]
