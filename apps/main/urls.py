from django.urls import path

from apps.main.views import HomeView, UserSearchView

urlpatterns = [
    path('', HomeView.as_view(), name='main'),
    path('search/', UserSearchView.as_view(), name='search-users'),


]
