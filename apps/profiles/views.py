from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from apps.profiles.models import Profile


class ProfileDetailTemplateView(LoginRequiredMixin, DetailView):
    template_name = 'main/profile.html'
    slug_field = 'username'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context
