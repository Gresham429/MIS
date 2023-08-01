"""
ASGI config for MIS project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import core.routing

os.environ["DJANGO_SETTINGS_MODULE"] = "MIS.settings"
django_application = get_asgi_application()


application = ProtocolTypeRouter({
    'http': django_application,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            core.routing.websocket_urlpatterns
        )
    ),
})


