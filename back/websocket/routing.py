# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/websocket/(?P<group>\w+)/(?P<user>\w+)/$", consumers.JsonConsumer.as_asgi()),
]
