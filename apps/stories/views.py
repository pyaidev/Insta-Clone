from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from apps.stories.models import Story, StoryContent


class CreateStoryView(View):

    def post(self, request):
        user = request.user.profile
        data = request.POST
        files = request.FILES.getlist('files')
        story = Story.objects.create(user=user)

        for file in files:
            StoryContent.objects.create(
                story=story,
                file=file
            )

        return redirect("/")

    def get(self, request):
        return render(request, 'main/create_story.html')


class StoriesDetail(TemplateView):
    template_name = "main/detail_story.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        username = kwargs.get('username', None)
        if not username:
            return context

        stories = Story.objects.filter(user__username=username,
                                       created_at__gte=timezone.now() - timezone.timedelta(hours=24))

        context['stories'] = stories
        return context
