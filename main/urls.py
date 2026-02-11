from django.urls import path

from .views import home, rooms, room,  create_room, update_room, delete_room

# Create your urls here.

app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
    path('rooms/', rooms, name='rooms'),
    path('rooms/<int:room_id>/', room, name='room'),
    path('rooms/create/', create_room, name='create-room'),
    path('rooms/update/<int:room_id>/', update_room, name='update-room'),
    path('rooms/delete/<int:room_id>/', delete_room, name='delete-room'),
]
