from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator

from apps.users.models import User
from apps.posts.models import Post, PostLike


class HomeView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user

        posts = Post.objects.filter(
            Q(user__profile__followers__followed_by__user=user) | Q(user=user)
        ).order_by('-created_at')

        like_indexes = PostLike.objects.filter(user=user).values_list('post__id', flat=True)

        return render(
            request, 'main/index.html',
            {
                'post_items': posts,
                'like_indexes': list(like_indexes),
            }
        )


class UserSearchView(View):
    def get(self, request):
        query = request.GET.get('q')
        context = {}
        if query:
            users = User.objects.filter(Q(username__icontains=query))

            paginator = Paginator(users, 8)
            page_number = request.GET.get('page')
            users_paginator = paginator.get_page(page_number)

            context = {
                'users': users_paginator,
            }
        return render(request, 'main/search.html', context)
