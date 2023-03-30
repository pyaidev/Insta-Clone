from django.shortcuts import render
from django.views import View

from apps.posts.models import Post
from .forms import PostForm


# Create your views here.
class PostDetailView(View):

    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        comments = post.comments.all()

        return render(
            request,
            'posts/post_detail.html',
            {'post': post, 'comments': comments}
        )


class PostCreateView(View):

    def get(self, request):

        post_form = PostForm()

        return render(
            request, 'main/new_post.html', {'post_form': post_form}
        )

    def post(self, request):
        post_form = PostForm(data=request.POST)

        return render(
            request,
            'posts/post_detail.html',
            # {'post': post, 'comments': comments}
        )

