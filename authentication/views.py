from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout  # for authentication

# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CustomUserCreationForm()

    if request.method == 'POST':
        utxt = request.POST.get('email')   # utxt to get/receive the username
        ptxt = request.POST.get('password')   # ptxt to get/receive the password   
        user = authenticate(username=utxt, password=ptxt) 
        if user != None:
            login(request, user)
            if request.user.is_staff and request.user.is_active:
                return redirect('home')
            else:
                return redirect('/')
        else:
            messages.warning(request,'{},username does not exist.'.format(utxt))

    return render(request, 'front/login.html', {'form':form})
##--#--## LogIn (mylogin) Function For Front (User Interface - Frontend) End ##--#--##

def registration_view(request):
    pass
@login_required
def logout_view(request):
    logout(request)
    return redirect('/')