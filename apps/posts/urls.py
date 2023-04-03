from django.urls import path

from .views import PostCreateView, PostDetailView, PostLikeView

app_name = 'posts'

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('<int:post_id>/detail/', PostDetailView.as_view(), name='post-detail'),
    path('<int:post_id>/like/', PostLikeView.as_view(), name='post-like'),

]
