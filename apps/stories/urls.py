from django.urls import path

from apps.stories.views import CreateStoryView, StoryDetailView

urlpatterns = [
    path('create/', CreateStoryView.as_view(), name='create_story'),
    path('detail/<str:username>/', StoryDetailView.as_view(), name='detail_story')
]
