from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import client_service.routing_channels

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,    
    'websocket': AuthMiddlewareStack(
        URLRouter(
            client_service.routing_channels.websocket_urlpatterns
        )
    ),
})