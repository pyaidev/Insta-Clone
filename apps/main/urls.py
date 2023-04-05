from django.urls import path

from apps.main.views import MainTemplateView, UserSearchView

urlpatterns = [
    path('', MainTemplateView.as_view(), name='main'),
    path('search/', UserSearchView.as_view(), name='search-users'),


]
