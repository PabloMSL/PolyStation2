from django.urls import path
from .views_ui import index_view, dashboard_comprador_view, dashboard_distribuidor_view

urlpatterns = [
    path('', index_view, name='store_ui'),
    path('dashboard-comprador/', dashboard_comprador_view, name='dashboard_comprador_ui'),
    path('dashboard-distribuidor/', dashboard_distribuidor_view, name='dashboard_distribuidor_ui'),
]
