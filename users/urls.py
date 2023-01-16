from django.urls import path, include
from .views import *

urlpatterns = [
    path('chat-page', chat_page, name='chat_page'),
    path('', login_page, name='login_page'),
    path('register', register_page, name='register_page'),
    ]
