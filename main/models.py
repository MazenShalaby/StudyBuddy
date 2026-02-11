from django.db import models
from django.conf import settings

# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'topic'
        verbose_name_plural = 'topics'
    
    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, related_name='topic_rooms')
    description = models.TextField()
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='room_participants') 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_at']
        verbose_name = 'room'
        verbose_name_plural = 'rooms'
        
        
class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_messages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.body[:50]}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'message'
        verbose_name_plural = 'messages'