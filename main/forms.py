from django.forms import ModelForm

from .models import Room, Message
# Create your froms here.


class RoomCreationForm(ModelForm):
    class Meta:
        model = Room
        fields = ('name', 'topic', 'description')
        
        
class UpdateMessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ('body',)
