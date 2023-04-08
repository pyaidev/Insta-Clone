import random

from django.core.cache import cache
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View

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


class RegisterView(View):

    def get(self, request):
        form = UsersCreationForm()

        return render(request, 'accounts/register.html', {"forms": form})

    def post(self, request):
        form = UsersCreationForm(request.POST)
        if form.is_valid():
            # form.save()
            data = form.cleaned_data
            email = data['email']
            code = get_random_string(length=4, allowed_chars='1234567890')
            session = get_random_string(length=16)
            send_sms_by_email(email, code)
            data.update({'code': code})
            cache.set(session, data, 300)
            response = redirect('verify_email')
            response.set_cookie('session', session)
            return response

        return render(request, 'accounts/register.html', {"forms": form})


def verify_email(request):
    if request.method == 'POST':
        r = request.POST
        code = r['num1'] + r['num2'] + r['num3'] + r['num4']
        session = request.COOKIES.get('session', None)
        if session is not None:
            session_data = cache.get(session)
            valid_code = session_data.pop('code')

            if valid_code == code:
                password = session_data.pop('password1')

                user = User(**session_data)
                user.is_active = True
                user.set_password(password)
                print(1)
                user.save()
                print(2)
                user = authenticate(password=password, username=user.username)
                login(request, user)
                print(3)
                messages.success(request, 'Your email has been verified. You are now logged in.')
                return redirect('profile_create')
            else:
                messages.error(request, "Incorrect code!", extra_tags='danger')
                return render(request, 'accounts/verificate.html')

    return render(request, 'accounts/verificate.html')


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
