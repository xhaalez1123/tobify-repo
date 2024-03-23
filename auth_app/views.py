from django.shortcuts import render, redirect, HttpResponse
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser as User
from .utils import send_email
import random
# Create your views here.


def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        email = request.POST.get('email')

        user = User.objects.filter(email=email)

        if user.exists():
            messages.info(request, "Already registered please login.")
            return redirect('/register/')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        user.set_password(password)
        user.save()
        login(request, user)
        if not user.is_verified:
            otp = random.randint(100000, 999999)
            user.otp = otp
            send_email(user, otp)
            user.save()
            messages.info(request, "Please verify your email")
            return redirect('/verify/')

    return render(request, 'register.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.info(request, "Invalide username")
            return redirect('/login/')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request, "Invalide password")
            return redirect('/login/')

        else:
            login(request, user)
            if not user.is_verified:
                messages.info(request, "Please verify your email")
                return redirect('/verify/')
            else:
                return redirect('/new/')

    return render(request, 'login.html')


@login_required(login_url='/login/')
def verify_email(request):
    user = request.user
    if user.is_verified:
        return redirect('/')
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if not User.objects.filter(id=user.id, otp=otp).exists():
            messages.error(request, "Invalid OTP for this user")
            return redirect('/verify/')

        # Clear OTP after successful verification
        user.is_verified = True
        user.otp = None
        user.save()
        # Redirect to home page or any other appropriate page
        return redirect('/')
    if not messages.get_messages(request):
        messages.success(request, "Verify your email.")
        messages.success(request, "Account Created successfully.")
    return render(request, 'verify.html')


def log_out(request):
    logout(request)
    return redirect('/login/')


@login_required(login_url='/login/')
def new_note(request):
    return HttpResponse('<h1>Successfully logged-in</h1><a href="/logout"><h1>Log-out</h1></a> ')


def home(request):
    user = request.user
    if user.is_authenticated:
        if not user.is_verified:
            messages.info(request, "Please verify your email")
            return redirect('/verify/')
    return render(request, 'index.html')
