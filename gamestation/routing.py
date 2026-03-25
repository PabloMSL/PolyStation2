from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
   # re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()), # Tu chat original
    re_path(r'ws/precios/$', consumers.PriceConsumer.as_asgi()), # Nueva ruta de precios
]