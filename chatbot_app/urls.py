from django.urls import path

from . import views

app_name = 'chatbot_app'
urlpatterns = [
    path('generate/', views.chatbot, name='chatbot'),
    path('clear-chats/', views.clear_chats, name='clear_chats'),
    path('', views.chatbot, name='chatbot'),
    path('get_chat_details/<int:session_id>/', views.get_chat_details, name='get_chat_details'),
    path('clear-one-chat/', views.clear_one_chat, name='clear_one_chat'),
]