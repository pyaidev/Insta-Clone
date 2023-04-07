from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UsersCreationForm
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


def register(request):
    form = UsersCreationForm()
    if request.method == "POST":
        form = UsersCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(password=password, username=username)
            login(request, user)
            return redirect('profile_create')

    return render(request, 'accounts/register.html', {"forms": form})


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

