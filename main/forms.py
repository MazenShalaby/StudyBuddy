from django.forms import ModelForm

from .models import Room
# Create your froms here.


class RoomCreationForm(ModelForm):
    class Meta:
        model = Room
        fields = ('host', 'name', 'topic', 'description', 'participants')