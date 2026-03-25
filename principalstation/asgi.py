import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import gamestation.routing # Importamos las rutas que acabamos de crear

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'principalstation.settings')

application = ProtocolTypeRouter({
    # Peticiones HTTP normales (tus POST, GET, PUT)
    "http": get_asgi_application(),
    
    # Conexiones en tiempo real (WebSockets)
    "websocket": AuthMiddlewareStack(
        URLRouter(
            gamestation.routing.websocket_urlpatterns
        )
    ),
})