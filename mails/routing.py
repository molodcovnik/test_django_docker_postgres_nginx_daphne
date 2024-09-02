from django.urls import re_path

from mails.consumers import EmailMessageConsumer, EmailCounterConsumer

websocket_urlpatterns = [
    re_path(r'^ws/(?P<account_id>\d+)/$', EmailMessageConsumer.as_asgi()),
    re_path(r'ws/(?P<account_id>\d+)/counter/$', EmailCounterConsumer.as_asgi()),
]