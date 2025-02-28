from django.urls import re_path
from system_metrics.consumers import SystemMetricsConsumer

websocket_urlpatterns = [
    re_path(r'ws/metrics/', SystemMetricsConsumer.as_asgi()),
]
