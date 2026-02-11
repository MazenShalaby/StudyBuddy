from django.contrib import admin

from .models import Topic, Room, Message

# Register your models here.

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    list_filter = ['name', 'created_at', 'updated_at']
    search_fields = ['name']
    
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'host', 'topic', 'description', 'created_at', 'updated_at']
    list_filter = ['topic']
    search_fields = ['name', 'topic']
    
    
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'room']
    list_filter = ['room']
    search_fields = ['user', 'created_at']