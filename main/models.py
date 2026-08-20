from django.db import models
from django.conf import settings

# Create your models here.

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Topic(TimeStampModel):
    name = models.CharField(max_length=255, db_index=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'topic'
        verbose_name_plural = 'topics'
    
    def __str__(self):
        return self.name


class Room(TimeStampModel):
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, related_name='topic_rooms')
    description = models.TextField()
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='room_participants') 
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_at']
        verbose_name = 'room'
        verbose_name_plural = 'rooms'
        
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['topic']),
            models.Index(fields=['host']),
        ]
        
        
class Message(TimeStampModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_messages')

    
    def __str__(self):
        return f"{self.body[:50]}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'message'
        verbose_name_plural = 'messages'