from django.urls import path
from .views import login_view, RegisterView, profile, verify_email

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', RegisterView.as_view(), name='register'),
    path('profile/', profile, name='profile_create'),
    path('verify/', verify_email, name='verify_email')
]
