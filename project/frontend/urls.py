from django.urls import path
from .views import (
    vista_index, vista_login,
    panel_usuario, panel_conductor,
    panel_admin
)

urlpatterns = [
    path('', vista_index, name='index'),
    path('login/', vista_login, name='login'),
    path('panel/usuario/', panel_usuario, name='panel_usuario'),
    path('panel/conductor/', panel_conductor, name='panel_conductor'),
    path('panel/admin/', panel_admin, name='panel_admin'),
    
    
]
