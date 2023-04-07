from django.urls import path

from apps.profiles.views import FollowView, UnfollowView, RemoveFollowerView, \
    RemoveFollowingView, ProfileDetailView, ProfileUpdateView, logout_user

app_name = "profiles"

urlpatterns = [
    path('<str:username>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('logout', logout_user, name='logout'),
    path('follow/', FollowView.as_view(), name='follow'),
    path('follow/<str:username>/', FollowView.as_view(), name='follow'),
    path('unfollow/<str:username>/', UnfollowView.as_view(), name='unfollow'),
    path('remove/follower/<str:username>/', RemoveFollowerView.as_view(), name='remove_follower'),
    path('remove/following/<str:username>/', RemoveFollowingView.as_view(), name='remove_following'),
    path('<str:username>/edit/', ProfileUpdateView.as_view(), name="edit-profile")
]
