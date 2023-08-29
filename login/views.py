from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from Arbisoft_Project import settings
from django.core.mail import send_mail

# Create your views here.
def home(request):
    return render(request, "login/index.html")

def signup(request):

    if request.method == "POST":
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists please try another username")
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request, "email already registered")
            return redirect('home')
        
        if len(username)>10:
            messages.error(request, "Username amust be under 10 characters")
            
        if pass1 != pass2:
            messages.error(request, "Passwords dont match")

        if not username.isalnum():
            messages.error(request, "Username must be alpha-numeric")
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your account is successfully created, we have sent an email")

        subject = "welcome hell"
        message = "hello" + myuser.first_name + "!!\n" + "Thank you for visiting my website\n we have sent a conformation email please confirm your email\n THANK YOU"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)


        return redirect('signin')


    return render(request, "login/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        pass1 = request.POST["pass1"]

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "login/index.html",{'fname': fname})
        else:
            messages.error(request, "Bad credientials")
            return redirect("home")
        
    return render(request, "login/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')


