from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView


class MainTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'main/index.html'
