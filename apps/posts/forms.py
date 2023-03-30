from django import forms

from apps.posts.models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('text', 'allow_commentary', )
        widgets = {'media': forms.ClearableFileInput(attrs={'multiple': True})}
