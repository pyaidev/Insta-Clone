import os

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

import apps.message.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.develop')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack((
            URLRouter(
                apps.message.routing.websocket_urlpatterns
            )
        ))
    )
})