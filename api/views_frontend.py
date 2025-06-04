from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def vista_index(request):
    """
    Muestra la página de inicio (index.html) sin requerir autenticación.
    """
    return render(request, 'api/index.html')
    # Busca project/templates/api/index.html

@login_required
def vista_panel(request):
    """
    Muestra la página de panel (panel.html) solo para usuarios autenticados.
    """
    return render(request, 'api/panel.html')
    # Busca project/templates/api/panel.html
