from django.shortcuts import render, redirect
from django.views import View

from apps.posts.models import Post, PostMedia
from apps.users.models import User
from .forms import PostForm


# Create your views here.
class PostDetailView(View):

    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        comments = post.comments.all()

        media_files = post.post_medias.all()

        return render(
            request,
            'posts/postdetail.html',
            {'post': post, 'comments': comments, 'media_files': media_files, 'media_range': range(media_files.count())}
        )


class PostCreateView(View):

    def get(self, request):

        post_form = PostForm()

        return render(
            request, 'main/new_post.html', {'post_form': post_form}
        )

    def post(self, request):
        post_form = PostForm(data=request.POST, files=request.FILES)

        if post_form.is_valid():
            post = post_form.save(commit=False)
            user = User.objects.all()[0]
            # post.user = request.user
            post.user = user
            post.save()

            media_files = request.FILES.getlist('media_files')

            for media in media_files:
                post_media = PostMedia.objects.create(post=post, file=media)

            # for video_file in videos:
            #     video = Video.objects.create(post=post, video=video_file)

            # return redirect('posts:post_detail', post_id=post.id)
            return redirect('posts:create')

