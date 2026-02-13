from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import HttpResponse

from .models import Topic, Room, Message
from .forms import RoomCreationForm, UpdateMessageForm
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return redirect('main:rooms')
    return render(request, 'main/home.html', context={})


####################################################### [Room] ####################################################


@login_required(login_url='accounts:login')
def rooms(request):
    rooms = Room.objects.select_related('topic')
    topics = Topic.objects.prefetch_related('topic_rooms')[:3] # limiting the topics to only 3 to be shown.
    recent_activity_messages = Message.objects.select_related('room')
    q = request.GET.get('q', '')
    
    if request.method == 'GET':
        rooms = rooms.filter(
            Q(name__icontains=q)|
            Q(host__username__icontains=q)|
            Q(topic__name__icontains=q)
            )
    
    context = {'rooms': rooms, 'topics': topics, 'recent_activity_messages': recent_activity_messages}
    return render(request, 'main/rooms.html', context)


@login_required(login_url='accounts:login')
def room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room_messages = room.room_messages.all()

    
    if request.method == 'POST':
        message_body = request.POST.get('msg', '')
        if message_body:
            new_message = Message.objects.create(
                user=request.user,
                room = room,
                body = message_body,
            )
            room.participants.add(new_message.user)
        else:
            messages.error(request, 'Message body must have a content and can\'t be left blank!') # show a msg to the user !
    context = {'room': room, 'room_messages': room_messages}
    return render(request, 'main/room.html', context)


@login_required(login_url='accounts:login')
def create_room(request):
    
    if request.method == 'POST':
        form = RoomCreationForm(data=request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.host = request.user
            new_form.save()
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

####################################################### [Browse Topics] ####################################################

@login_required(login_url='accounts:login')
def browse_topics(request):

    q = request.GET.get('q', '')
    topics = (
        Topic.objects
        .filter(name__icontains=q)
        .annotate(rooms_count=Count('topic_rooms')) # For preventing N+1 queries while counting each topic's rooms, In the template we use that annotate attr {{topic.rooms_count}}
    )
    
    context = {'rooms': rooms, 'topics': topics}
    return render(request, 'main/browse_topics.html', context)

####################################################### [Message] ####################################################


@login_required(login_url='main:login')
def delete_message(request, msg_id):
    
    message = get_object_or_404(Message, id=msg_id)
    room = message.room
    if request.user == message.user:
        if request.method == 'POST':
            message.delete()
            return redirect('main:room', room_id=room.id)
    else:
        return HttpResponse("Your are not allowed to perform his action!")
    
    context = {'message': message, 'room': room}
    return render(request, 'main/delete_message.html', context)


@login_required(login_url='main:login')
def update_message(request, msg_id):
    
    message = get_object_or_404(Message, id=msg_id)
    room = message.room
    form = UpdateMessageForm(instance=message)
    if request.user == message.user:
        if request.method == 'POST':
            form = UpdateMessageForm(data=request.POST, instance=message)
            if form.is_valid():
                user = form.save(commit=False)
                user.user = request.user
                user.save()
                return redirect('main:room', room_id=room.id)
            else:
                messages.error(request, "An error has been occured during updating the message!")
    else:
        return HttpResponse("Your are not allowed to perform his action!")
    
    context = {'message': message, 'room': room, 'form': form}
    return render(request, 'main/update_message.html', context)