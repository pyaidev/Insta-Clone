from django.urls import path
from .views import login_view, register, profile

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', register, name='register'),
    path('profile/', profile, name='profile_create')
]
