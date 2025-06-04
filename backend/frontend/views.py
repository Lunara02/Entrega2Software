# backend/frontend/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def vista_index(request):
    return render(request, 'frontend/index.html')

@login_required(login_url='/')
def vista_panel(request):
    return render(request, 'frontend/panel.html')
