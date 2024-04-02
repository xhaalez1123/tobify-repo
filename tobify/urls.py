"""
URL configuration for tobify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from auth_app.views import *
from skapi.views import cheker
urlpatterns = [
    path('admin-tobi-tech/', admin.site.urls),
    path('skapi/', cheker, name='cheker'),
    path('register/', register_page, name='register_page'),
    path('login/', login_page, name='login_page'),
    path('verify/', verify_email, name='verify_email'),
    path('resend/', resend_mail, name='resend_mail'),
    path('new/', new_note, name='new_note'),
    path('about/', about, name='about'),
    path('note/<str:pk>/', note_detail, name='note_detail'),
    path('logout/', log_out, name='logout'),
    path('', home, name='home')
]
