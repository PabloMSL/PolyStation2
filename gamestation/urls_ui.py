from django.urls import path
from .views_ui import index_view

urlpatterns = [
    path('', index_view, name='store_ui'),
]
