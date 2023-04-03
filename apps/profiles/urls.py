from django.urls import path

from apps.profiles.views import ProfileDetailTemplateView, FollowView

app_name = "profiles"

urlpatterns = [
    path('<str:username>/', ProfileDetailTemplateView.as_view(), name='profile_detail'),
    path('follow/', FollowView.as_view(), name='follow')
]
