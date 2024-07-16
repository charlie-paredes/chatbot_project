from django.db import models
from django.contrib.auth.models import User

#represents the chat session, which is a collection of chat messages
class ChatSession(models.Model):
    character_choice = models.CharField(max_length=255)
    media_choice = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Session with {self.character_choice} from {self.media_choice} at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

#represents the chat message
class ChatMessage(models.Model):
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    user_input = models.TextField()
    generated_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from session {self.chat_session.id} at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"