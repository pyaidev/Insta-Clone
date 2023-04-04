from django.forms import ModelForm

from apps.profiles.models import Profile


class ProfileCreationForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('image', 'bio', 'gender')

