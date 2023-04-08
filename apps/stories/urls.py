from django.urls import path

from apps.stories.views import CreateStoryView

urlpatterns = [
    path('create/', CreateStoryView.as_view(), name='create_story')
]
