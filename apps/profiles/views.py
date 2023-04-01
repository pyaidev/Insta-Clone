from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, DetailView

from apps.posts.models import Post, PostMedia
from apps.profiles.models import Profile, Follower


class ProfileDetailTemplateView(LoginRequiredMixin, DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'main/profile.html'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return Profile.objects.filter(user__username=username).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.filter(user=self.request.user).first()
        followers = Follower.objects.filter(followed_to__user=self.request.user).count()
        post = PostMedia.objects.filter(post__user=self.request.user).values('file', 'media_type')

        # post_count = Post.objects.values('likes_count', 'comments_count')

        context['followers'] = followers
        context['profile'] = profile
        context['posts'] = post
        # context['posts_count'] = post_count

        return context
