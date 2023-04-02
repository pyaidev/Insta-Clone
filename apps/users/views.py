from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UsersCreationForm


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
            return redirect('main')

    return render(request, 'accounts/register.html', {"forms": form})


# def logout_user(request):
#     logout(request)
#     messages.warning(request, 'You have been logged out!')
#     return redirect('login')