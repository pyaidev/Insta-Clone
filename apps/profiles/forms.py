from django.forms import ModelForm, CharField, EmailField

from apps.profiles.models import Profile


class ProfileCreationForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('image', 'bio', 'gender')


class EditProfileForm(ModelForm):
    username = CharField()
    email = EmailField()

    class Meta:
        model = Profile
        fields = ('image', 'bio', 'gender', 'username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = self.instance.user.username
        self.fields['email'].initial = self.instance.user.email
        self.fields['username'].label = 'Username'
        self.fields['email'].label = 'Email'