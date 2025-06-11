from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.
def register(request):
    if request.method == "POST":
        # get data from form
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # password match check
        if password != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('register')
        else:
            # all good
            newUser = User.objects.create_user(password=password, email=email, first_name=first_name, last_name=last_name)
            # save user
            newUser.save()
            messages.success(request, "You are noew registered and can log in!")
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')
    
def login(request):
    if request.method == "POST":
        # login the user
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are successfully logged in!")
            # idk abt this check laters !!!!!!!!!
            return redirect("index")
        else:
            messages.error(request, "Invalid credentials! Try again!")
            return redirect("login")
    else:
        return render(request, 'accounts/login.html')
    
def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, "You are now logged out!")
        return redirect("index")