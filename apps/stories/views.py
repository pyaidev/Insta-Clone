from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from apps.stories.models import Story, StoryContent


class CreateStoryView(View):
    def get(self, request):
        return render(request, 'main/create_story.html')

    def post(self, request):
        user = request.user.profile
        files = request.FILES.getlist('files')
        story = Story.objects.create(user=user)

        for file in files:
            StoryContent.objects.create(
                story=story,
                file=file
            )

        return redirect("/")


class StoryDetailView(TemplateView):
    template_name = "main/story_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stories = Story.objects.filter(
            created_at__gte=timezone.now() - timezone.timedelta(hours=24),
            user__user__username=self.kwargs['username']
        )

        context['stories'] = stories
        return context
