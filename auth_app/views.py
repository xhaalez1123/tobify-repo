from django.shortcuts import render, redirect, HttpResponse
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser as User, note as Note
from .utils import send_email
import random
# Create your views here.


def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # check weather the email in currect format or not
        if "@" not in email or "." not in email.split("@")[1]:
            messages.info(request, "Invalide email")
            return redirect('/register/')

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
        email = request.POST.get('email')
        password = request.POST.get('password')

        if "@" not in email or "." not in email.split("@")[1]:
            messages.info(request, "Invalide email")
            return redirect('/login/')

        if not User.objects.filter(email=email).exists():
            messages.info(request, "Invalide Email")
            return redirect('/login/')

        user = authenticate(email=email, password=password)

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
    if not request.user.is_verified:
        messages.info(request, "Please verify your email")
        return redirect('/verify/')
    if request.method == 'POST':
        note_new = Note()
        note_new.title = request.POST.get('note_title')
        note_new.content = request.POST.get('note_content')
        note_new.author = request.user
        note_new.id = note_new.title[:10] + \
            '-' + str(random.randint(1000, 9999))
        note_new.save()
        return redirect('/note/' + str(note_new.id))
    return render(request, 'new.html')


def note_detail(request, pk):
    try:
        note_instance = Note.objects.get(id=pk)
    except Note.DoesNotExist:
        return HttpResponse("Note not found", status=404)

    return render(request, 'note.html', {'note': note_instance})


def home(request):
    user = request.user
    if user.is_authenticated:
        if not user.is_verified:
            messages.info(request, "Please verify your email")
            return redirect('/verify/')
    return render(request, 'index.html')


@login_required(login_url='/login/')
def resend_mail(request):
    user = request.user
    if user.is_verified:
        return redirect('/')
    otp = random.randint(100000, 999999)
    user.otp = otp
    send_email(user, otp)
    user.save()
    messages.info(request, "OTP sent to your email")
    return redirect('/verify/')
