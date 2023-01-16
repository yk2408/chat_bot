from django.urls import path, include
from .views import *

urlpatterns = [
    path('chat-page', chat_page, name='chat_page'),
    ]
