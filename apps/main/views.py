from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from apps.users.models import User
from django.core.paginator import Paginator
from django.db.models import Q


class MainTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'main/index.html'

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