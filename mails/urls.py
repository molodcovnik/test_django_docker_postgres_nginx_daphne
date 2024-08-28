from django.urls import path
from mails.views import index


urlpatterns = [
    path('', index, name='home'),
]