from django.contrib import admin

# Register your models here.
from .models import ChatSession, ChatMessage

admin.site.register(ChatMessage)

admin.site.register(ChatSession)