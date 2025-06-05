from django.urls import path
from .views import vista_index, vista_panel, vista_logout

urlpatterns = [
    # '' (vacío) será la página de login
    path('', vista_index, name='home'),
    # Panel protegido
    path('panel/', vista_panel, name='panel'),
    # Logout
    path('logout/', vista_logout, name='logout'),
]
