from django.urls import path

from .views import PostCreateView, PostDetailView

app_name = 'posts'

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='create'),
    path('<int:post_id>/detail/', PostDetailView.as_view(), name='detail'),

]
