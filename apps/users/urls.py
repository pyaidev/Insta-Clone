from django.urls import path
from .views import login_view, register, profile, verify_email

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', register, name='register'),
    path('profile/', profile, name='profile_create'),
    path('verificate/', verify_email, name='verify_email')
]
