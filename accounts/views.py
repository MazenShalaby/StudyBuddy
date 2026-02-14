from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.contrib.auth import get_user_model
from django.http import HttpResponse

from main.models import Topic, Room, Message 
from .forms import CustomUserCreationForm, CustomUserChangeForm, LoginForm


# Create your views here.

####################################################### [Authentication] ####################################################

def register(request): 
    
    page = 'register'
    
    if request.user.is_authenticated:
        return redirect('main:rooms')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('main:rooms')
        else:
            messages.error(request, "An error has been occured during registration!")
    else:
        form = CustomUserCreationForm()
        
    context = {'form': form, 'page': page}
    return render(request, 'accounts/login_register.html', context)


def login_view(request):
    
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('main:rooms')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect("main:rooms")
            else:
                raise ValueError("User does not exist!")
        
        else:           
            messages.error(request, "An error has been occured during login!")
            
    else:
        form = LoginForm()
    
    context = {'form': form, 'page': page}
    return render(request, 'accounts/login_register.html', context)


def logout_view(request):
    logout(request)
    return redirect('main:home')

####################################################### [User Profile] ####################################################

@login_required(login_url='accounts:login')
def user_profile(request, user_id):
    
    user = get_object_or_404(get_user_model(), id=user_id)
    q = request.GET.get('q', '')
    user_topics = (
        Topic.objects
        .filter(topic_rooms__host=user)
        .annotate(rooms_count=Count('topic_rooms'))
    )
    rooms = Room.objects.select_related('topic').filter(host=user, topic__name__icontains=q)
    recent_activity_messages = Message.objects.select_related('room').filter(user=user)
    
    context = {'user': user, 'user_topics':user_topics, 'rooms': rooms, 'recent_activity_messages': recent_activity_messages}
    return render(request, 'accounts/user_profile.html', context)


@login_required(login_url='accounts:login')
def update_profile(request, user_id):
    
    user = get_object_or_404(get_user_model(), id=user_id)
    if request.user == user:
        if request.method == 'POST':
            form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                return redirect('accounts:profile', user_id=user_id)
            else:
                messages.error("An error has been occured during profile update!")
        else:
            form = CustomUserChangeForm(instance=user)
    else:
        return HttpResponse("Your are not allowed to perform this action")
    
    context = {'form': form}
    return render(request, 'accounts/update_profile.html', context)

################################################################################################################

@login_required(login_url='accounts:login')
def browse_user_topics(request, user_id):
    
    user = get_object_or_404(get_user_model(), id=user_id)
    topics = Topic.objects.filter(topic_rooms__host=user)
    q = request.GET.get('q', '')
    if request.method == 'GET':
        topics = (
        Topic.objects
        .filter(name__icontains=q, topic_rooms__host=user)
        .annotate(rooms_count=Count('topic_rooms'))
    )
    
    context = {'user': user, 'topics': topics}
    return render(request, 'accounts/user_topics.html', context)