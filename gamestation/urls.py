from django.urls import path
from .views_comprador import *
from .views_distribuidor import *

urlpatterns = [

# HOME

path('', catalogo, name='catalogo'),

# COMPRADOR

path('registro/', registro_comprador, name='registro_comprador'),
path('login/', login_comprador, name='login_comprador'),
path('biblioteca/', biblioteca, name='biblioteca'),
path('comprar/<str:juego_id>/', comprar_juego, name='comprar_juego'),
path('resena/<str:juego_id>/', crear_resena, name='crear_resena'),