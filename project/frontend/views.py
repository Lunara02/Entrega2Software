from django.shortcuts import render
from django.conf import settings

def vista_index(request):
    return render(request, 'index.html')

def vista_login(request):
    return render(request, 'login.html')

def panel_usuario(request):
    return render(request, 'panel_usuario.html')

def panel_conductor(request):
    return render(request, 'panel_conductor.html')


def panel_admin(request):
    return render(request, 'panel_admin.html', {'MAPBOX_TOKEN': settings.MAPBOX_TOKEN})
