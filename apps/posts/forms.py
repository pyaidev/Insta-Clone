from django import forms

from apps.posts.models import Post


class PostForm(forms.ModelForm):
    media_files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Post
        fields = ('text', 'allow_commentary',)
