from django.urls import path

from apps.stories.views import StoryTemplateView

urlpatterns = [
    path('', StoryTemplateView.as_view(), name='story')
]
