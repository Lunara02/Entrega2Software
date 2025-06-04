# backend/frontend/urls.py
from django.urls import path
from .views import vista_index, vista_panel

urlpatterns = [
    path('', vista_index, name='home'),
    path('panel/', vista_panel, name='panel'),
]
