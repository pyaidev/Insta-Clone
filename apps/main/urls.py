from django.urls import path

from apps.main.views import MainTemplateView

urlpatterns = [
    path('', MainTemplateView.as_view(), name='main')

]
