from django.urls import path

from apps.profiles.views import ProfileDetailTemplateView, FollowView, UnfollowView, RemoveFollowerView, \
    RemoveFollowingView

app_name = "profiles"

urlpatterns = [
    path('<str:username>/', ProfileDetailTemplateView.as_view(), name='profile_detail'),
    path('follow/', FollowView.as_view(), name='follow'),

    path('follow/<str:username>/', FollowView.as_view(), name='follow'),
    path('unfollow/<str:username>/', UnfollowView.as_view(), name='unfollow'),
    path('remove/follower/<str:username>/', RemoveFollowerView.as_view(), name='remove_follower'),
    path('remove/following/<str:username>/', RemoveFollowingView.as_view(), name='remove_following')
]
