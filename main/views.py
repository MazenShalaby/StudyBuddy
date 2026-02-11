from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse

from .models import Topic, Room, Message
from .forms import RoomCreationForm
# Create your views here.


def home(request):
    return render(request, 'main/home.html', context={})

####################################################### [Rooms] ####################################################

@login_required(login_url='accounts:login')
def rooms(request):
    rooms = Room.objects.select_related('topic')
    topics = Topic.objects.prefetch_related('topic_rooms')
    
    q = request.GET.get('q', '')
    
    if request.method == 'GET':
        rooms = rooms.filter(
            Q(name__icontains=q)|
            Q(host__username__icontains=q)|
            Q(topic__name__icontains=q)
            )
    
    context = {'rooms': rooms, 'topics': topics}
    return render(request, 'main/rooms.html', context)


@login_required(login_url='accounts:login')
def room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room_messages = room.room_messages.all()
    
    context = {'room': room, 'room_messages': room_messages}
    return render(request, 'main/room.html', context)


@login_required(login_url='accounts:login')
def create_room(request):
    if request.method == 'POST':
        form = RoomCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:rooms')
        else:
            messages.error(request, "An error has been occured during room creation!")
    else:
        form = RoomCreationForm()
        
    context = {'form': form}
    return render(request, 'main/create_room.html', context)


@login_required(login_url='accounts:login')
def update_room(request, room_id):
    
    room = get_object_or_404(Room, id=room_id)
    form = RoomCreationForm(instance=room)
    if request.user == room.host:
        if request.method == 'POST':
            form = RoomCreationForm(data=request.POST, instance=room)
            if form.is_valid():
                form.save()
                return redirect("main:room", room_id=room_id)
            else:
                return HttpResponse("An error has been occured during room update!")
    else:
        return HttpResponse("You are not allowed to perform this action!")
        
    context = {'form': form}
    return render(request, 'main/update_room.html', context)


@login_required(login_url='accounts:login')
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.user == room.host:
        if request.method == 'POST':
            room.delete()
            return redirect('main:rooms')
    else:
        return HttpResponse("You are not allowed to perform this action!")
        
    context = {'room': room}
    return render(request, 'main/delete_room.html', context)