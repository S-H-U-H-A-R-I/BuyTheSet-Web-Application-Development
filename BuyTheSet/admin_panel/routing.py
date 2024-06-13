from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from .products_consumer.products_consumer import ProductConsumer
from .chat_consumer import ChatConsumer

websocket_urlpatterns = [
    re_path(r'^admin_panel/ws/products/', AuthMiddlewareStack(ProductConsumer.as_asgi())),
    re_path(r'^admin_panel/ws/chat/', AuthMiddlewareStack(ChatConsumer.as_asgi())),
]