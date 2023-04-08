from django.shortcuts import render
from django.views.generic import TemplateView


class StoryTemplateView(TemplateView):
    template_name = 'main/detail_story.html'