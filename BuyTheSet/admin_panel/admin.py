from django.contrib import admin
from .models import AIChat, ChatMessages


class ChatMessagesInline(admin.TabularInline):
    model = ChatMessages
    extra = 0
    
@admin.register(AIChat)
class AIChatAdmin(admin.ModelAdmin):
    inlines = [ChatMessagesInline]
    list_display = ['user',]
    search_fields = ['user__username']