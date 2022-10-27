from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'home.html')

def login(request):

    if request.user.is_authenticated:
        return redirect('home')

    
    if request.method == "POST" :

        try:
            username = request.POST['username']
            password = request.POST['pass1']
            user = authenticate(username = username, password=password)
            
            if user is not None:
                auth_login(request, user)
                return redirect('home')

        except MultiValueDictKeyError:
            return HttpResponse(content="make Valid Inputs")

    return render(request, 'login.html')

def register(request):

    context = {
        'message': None
    }

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST" :

        try:
            name = request.POST['name']
            name = name.split(' ')
            first_name = name[0]
            last_name = name[:-1]
            username = request.POST['username']
            email = request.POST['email']
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']



        except MultiValueDictKeyError:
            context['message'] = 'Please Fill all the fields'
            messages.error(request, 'Please Fill all the fields' )
            return redirect('register')

        if pass1 != pass2 :
            context['message'] = 'Your password and confirm password doesnot match'
            messages.error(request, 'Your password and confirm password doesnot match' )
            return redirect('register')

        if User.objects.filter(username = username):
            context['message'] = 'Username Already exists'
            messages.error(request, 'Username Already exists' )
            return redirect('register')

        if User.objects.filter(email = email):
            context['message'] = 'Email Already exists'
            messages.error(request, 'Email Already exists' )
            return redirect('register')
        
        user = User.objects.create_user(username=username, email=email, password=pass1)
        user.first_name = first_name
        user.last_name = last_name

        user.save()
        return redirect('login')

    return render(request, 'register.html')

def signout(request):
    logout(request)
    return redirect('home')
