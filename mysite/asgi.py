import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from .middleware import TokenAuthMiddleware
from notifications.routing import ws_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': TokenAuthMiddleware(
            URLRouter(
                ws_urlpatterns
            )
        )
    }
)
