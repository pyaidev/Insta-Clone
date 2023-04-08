import random

from django.core.cache import cache
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.utils.crypto import get_random_string

from .forms import UsersCreationForm
from .models import User
from .utils import send_sms_by_email
from ..profiles.forms import ProfileCreationForm
from ..profiles.models import Profile


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.success(request, 'Please enter correct credentials...!')
            return redirect('login')

    return render(request, 'accounts/login.html', {})


# def register(request):
#     form = UsersCreationForm()
#     if request.method == "POST":
#         form = UsersCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             email = form.cleaned_data['email']
#
#             user = authenticate(password=password, username=username)
#             login(request, user)
#             code = get_random_string(length=4, allowed_chars='1234567890')
#             send_sms_by_email(email, code)
#
#             return redirect('verify_email')
#
#     return render(request, 'accounts/register.html', {"forms": form})


# def verify_email(request):
#     if request.method == 'POST':
#         r = request.POST
#         code = r['num1'] + r['num2'] + r['num3'] + r['num4']
#         user = cache.get('user')
#
#         if cache.get('session') == r['session'] and cache.get('code') == code:
#             user = User.objects.get(email=user['email'])
#             user.is_active = True
#             user.save()
#             login(request, user)
#             messages.success(request, 'Your email has been verified. You are now logged in.')
#             return redirect('profile_create')
#         else:
#             messages.error(request, 'The verification code you entered is incorrect. Please try again.')
#
#     return render(request, 'accounts/verificate.html')


def profile(request):
    form = ProfileCreationForm()
    if request.method == "POST":
        form = ProfileCreationForm(request.POST)
        if form.is_valid():
            Profile.objects.create(
                user=request.user,
                image=form.cleaned_data['image'],
                bio=form.cleaned_data['bio'],
                gender=form.cleaned_data['gender']
            )

            return redirect('profiles:profile_detail', username=request.user.username)

    return render(request, 'accounts/profile.html', {"forms": form})
