import uuid
from django.contrib.auth.models import User
from django.db import models


class AIChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat')
    api_key = models.CharField(max_length=100, default='')
    
    def __str__(self):
        return f"Chat for user {self.user.username}"


class ChatMessages(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat = models.ForeignKey(AIChat, on_delete=models.CASCADE, related_name='messages')
    chat_history = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    system_message = models.CharField(max_length=255, default='You are an AI assistant, eager to help the user!', null=True, blank=True)
    
    def __str__(self):
        return f"Chat message {self.id} for chat {self.chat.id}"
