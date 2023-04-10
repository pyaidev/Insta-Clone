from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DetailView, UpdateView

from apps.posts.models import Post, PostMedia
from apps.profiles.models import Profile, Follower

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from .forms import ProfileCreationForm, EditProfileForm
from .models import Profile, Follower
from ..users.models import User


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'main/profile.html'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        profile = get_object_or_404(Profile, user__username=username)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()

        # followers
        followers = profile.get_followers()
        context['followers'] = followers
        # followings
        followings = profile.get_followings()
        context['followings'] = followings
        # posts
        posts = Post.objects.filter(user__username=self.kwargs.get('username')).order_by('-created_at')
        context['posts'] = posts

        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = EditProfileForm
    slug_field = 'user__username'
    slug_url_kwarg = 'username'
    template_name = 'main/edit_profile.html'
    success_url = reverse_lazy('profiles:profile-detail')

    def get_success_url(self):
        return reverse_lazy('profiles:profile_detail', args=[self.request.user.username])

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.user != self.request.user:
            raise Http404
        return obj

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def logout_user(request):
    logout(request)
    messages.warning(request, 'You have been logged out!')
    return redirect('login')


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
