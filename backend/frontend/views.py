from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def vista_index(request):
    """
    Si llega por GET: mostrar el formulario de login.
    Si llega por POST: intentar autenticar con username/password.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('panel')
        else:
            # Agrega un mensaje de error que se mostrará en la plantilla
            messages.error(request, 'Usuario o contraseña inválidos.')

    return render(request, 'frontend/index.html')


@login_required(login_url='home')
def vista_panel(request):
    """
    Vista protegida que solo muestra el panel si el usuario está autenticado.
    En caso de que necesites procesar otros formularios (creación de paquete, etc.),
    podrías detectar aquí request.method == 'POST' y manejarlo.
    Por simplicidad, dejamos solo el render del template.
    """
    return render(request, 'frontend/panel.html')


def vista_logout(request):
    """
    Desconecta al usuario y lo redirige al login.
    """
    logout(request)
    return redirect('home')
