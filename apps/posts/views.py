import magic
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


from apps.posts.models import Post, PostMedia
from apps.posts.choices import MediaTypes
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
            'posts/post_detail.html',
            {'post': post, 'comments': comments, 'media_files': media_files, 'media_range': range(media_files.count())}
        )


class PostCreateView(LoginRequiredMixin, View):

    def get(self, request):

        post_form = PostForm()

        return render(
            request, 'posts/new_post.html', {'post_form': post_form}
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
                mime_type = magic.from_buffer(media.read(), mime=True)
                if mime_type.startswith('video/'):
                    media_type = MediaTypes.VIDEO
                elif mime_type.startswith('image/'):
                    media_type = MediaTypes.IMAGE
                else:
                    messages.error(request, "Incorrect media type!", extra_tags='danger')
                    return render(
                        request, 'posts/new_post.html', {'post_form': post_form}
                    )

                PostMedia.objects.create(post=post, file=media, media_type=media_type)

            return redirect('posts:post-detail', post_id=post.id)

        # if Form is not valid
        return render(
            request, 'posts/new_post.html', {'post_form': post_form}
        )
