from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DetailView

from apps.posts.models import Post, PostMedia
from apps.profiles.models import Profile, Follower

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .models import Profile, Follower


class ProfileDetailTemplateView(LoginRequiredMixin, DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'main/profile.html'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        profile = Profile.objects.get(user__username=username)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        followers = Follower.objects.filter(followed_to__user=user).count()
        post = PostMedia.objects.filter(post__user__username=self.kwargs.get('username')).values('file',
                                                                                                 'media_type').order_by(
            '-created_at')

        context['followers'] = followers
        context['profile'] = self.get_object()
        context['posts'] = post

        return context


class FollowView(LoginRequiredMixin, View):
    http_method_names = ['post']

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        profile_id = request.POST.get('profile_id')
        action = request.POST.get('action')

        if profile_id and action:
            try:
                profile = Profile.objects.get(id=profile_id)
                if action == 'follow':
                    Follower.objects.get_or_create(followed_by=request.user.profile, followed_to=profile)
                else:
                    Follower.objects.filter(followed_by=request.user.profile, followed_to=profile).delete()
                return JsonResponse({'status': 'ok'})
            except Profile.DoesNotExist:
                pass

        return JsonResponse({'status': 'error'})
