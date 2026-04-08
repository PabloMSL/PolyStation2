from django.shortcuts import render

def index_view(request):
    return render(request, 'gamestation/index.html')

def dashboard_comprador_view(request):
    return render(request, 'gamestation/dashboard_comprador.html')

def dashboard_distribuidor_view(request):
    return render(request, 'gamestation/dashboard_distribuidor.html')
