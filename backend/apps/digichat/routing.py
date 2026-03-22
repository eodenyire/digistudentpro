from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/squad/(?P<squad_slug>\w+)/$', consumers.SquadChatConsumer.as_asgi()),
    re_path(r'ws/chat/dm/(?P<user_id>\d+)/$', consumers.DirectMessageConsumer.as_asgi()),
]
