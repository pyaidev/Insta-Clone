from django import forms

from apps.posts.models import Post, Comment


class PostForm(forms.ModelForm):
    media_files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=True)

    class Meta:
        model = Post
        fields = ('text', 'allow_commentary',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text', )
