from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout  # for authentication

# Create your views here.
def login_view(request):
    """
    Handle user login functionality.

    If the user is already authenticated, redirect them to the 'home' page.
    If the request method is 'POST', attempt to authenticate the user using the provided username and password.
    If the authentication is successful, log in the user, and redirect them to the 'home' page if they are a staff member and active.
    If the authentication fails, display a warning message indicating that the username does not exist.
    If the user is not authenticated and the request method is not 'POST', render the 'front/login.html' template with the login form.

    Args:
        request: The HTTP request object.

    Returns:
        - If the user is already authenticated, a redirect to the 'home' page.
        - If the authentication is successful and the user is a staff member and active, a redirect to the 'home' page.
        - If the authentication fails, a redirect to the '/' (root) URL.
        - If the user is not authenticated and the request method is not 'POST', the rendered 'front/login.html' template with the login form.

    Note:
        - This view assumes the use of Django's render and redirect functions.
        - The 'CustomUserCreationForm' is a custom form for user creation, assumed to exist.
        - The 'authenticate' and 'login' functions are from Django's authentication framework.
        - The 'messages' module is assumed to be imported from Django for displaying warning messages.
        - The 'front/login.html' template is expected to exist and contain the necessary markup for the login form.
    """
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

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')