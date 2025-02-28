import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from system_metrics.consumers import SystemMetricsConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "personalWebpage.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                re_path(r'ws/metrics/', SystemMetricsConsumer.as_asgi()),
            ]
        )
    ),
})