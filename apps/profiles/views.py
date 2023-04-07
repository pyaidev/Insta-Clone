from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DetailView

from apps.posts.models import Post, PostMedia
from apps.profiles.models import Profile, Follower

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from .forms import ProfileCreationForm
from .models import Profile, Follower
from ..users.models import User


class ProfileDetailTemplateView(LoginRequiredMixin, DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'main/profile.html'

    def get_object(self, queryset=None):
        print(1)
        username = self.kwargs.get('username')
        profile = Profile.objects.get(user__username=username)
        print(2)
        return profile

    def get_context_data(self, **kwargs):
        print(3)
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        print(4)
        followers = Follower.objects.filter(followed_to=profile)
        post = Post.objects.filter(user__username=self.kwargs.get('username')).order_by('-created_at')
        print(5)
        context['followers_count'] = followers.count()
        context['followers'] = followers

        print(6)
        context['profile'] = profile
        context['posts'] = post

        print(7)
        if self.request.user.is_authenticated:
            user_follow = Follower.objects.filter(followed_by=self.request.user.profile, followed_to=profile).exists()
            context['user_follow'] = user_follow

        return context


class FollowView(View):

    def get(self, request, username):
        return redirect(request.META.get('HTTP_REFERER'))

    def post(self, request, username):
        following = get_object_or_404(User, username=username)
        profile_2 = Profile.objects.get(user=following)
        profile = Profile.objects.get(user=self.request.user)
        Follower.objects.update_or_create(followed_by=profile, followed_to=profile_2)
        return redirect(request.META.get('HTTP_REFERER'))


class UnfollowView(View):

    def get(self, request, username):
        return redirect(request.META.get('HTTP_REFERER'))

    def post(self, request, username):
        following = get_object_or_404(User, username=username)
        profile_2 = Profile.objects.get(user=following)
        profile = Profile.objects.get(user=self.request.user)
        user_follow = Follower.objects.filter(followed_by=profile, followed_to=profile_2).first()
        if user_follow is not None:
            user_follow.delete()

        return redirect(request.META.get('HTTP_REFERER'))


class RemoveFollowerView(View):

    def get(self, request, username):
        return redirect(request.META.get('HTTP_REFERER'))

    def post(self, request, username):
        following = get_object_or_404(User, username=username)
        following2 = Profile.objects.get(user=following)
        profile = Profile.objects.get(user=self.request.user)
        user_follow = Follower.objects.filter(followed_by=following2, followed_to=profile).first()
        if user_follow is not None:
            user_follow.delete()

        return redirect(request.META.get('HTTP_REFERER'))


class RemoveFollowingView(View):

    def get(self, request, username):
        return redirect(request.META.get('HTTP_REFERER'))

    # def post(self, request, username):
    #     following = get_object_or_404(User, username=username)
    #     following2 = Profile.objects.get(user=following)
    #     profile = Profile.objects.get(user=self.request.user)
    #     user_follow = Follower.objects.filter(followed_by=profile, followed_to=following2).first()
    #     if user_follow is not None:
    #         user_follow.delete()
    #
    #     return redirect(request.META.get('HTTP_REFERER'))


