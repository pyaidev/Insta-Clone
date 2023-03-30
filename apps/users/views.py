from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm


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


def register_view(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            print(username)
            try:
                user = authenticate(password=password, username=username)
            except Exception as e:
                messages.success(request, e)
            login(request, user)
            return redirect('main')

    return render(request, 'accounts/register.html', {"forms": form})
