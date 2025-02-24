from django.urls import path, include
from .views import chat_page

urlpatterns = [
    path('api/', include('chat.api.urls')), 
    path('', chat_page, name='chat-page')
]
