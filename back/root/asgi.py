"""
ASGI config for root project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from root.consumers import ChatConsumer
from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')
django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter({  # 可以直接把routing的app写到这,就不用get_default_application和在settings设置ASGI_APPLICATION了
    'websocket':
    SessionMiddlewareStack(  # 用于websocket请求
        URLRouter([  # 绑定websocket地址
            path('ws/group/<slug:group>/<str:user>/', ChatConsumer.as_asgi()),  # 不知道为啥要用as_asgi
        ])),
    "http":
    django_asgi_app,  # 用于普通请求
})
