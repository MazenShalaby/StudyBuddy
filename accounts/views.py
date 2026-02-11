from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, LoginForm

# Create your views here.

####################################################### [Authentication] ####################################################

def register(request): 
    
    page = 'register'
    
    if request.method == 'POST':
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('main:rooms')
        else:
            messages.error(request, "An error has been occured during room update!")
    else:
        form = CustomUserCreationForm()
        
    context = {'form': form, 'page': page}
    return render(request, 'accounts/login_register.html', context)


def login_view(request):
    
    page = 'login'
    
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
