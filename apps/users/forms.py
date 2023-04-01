from .models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class UsersCreationForm(UserCreationForm):
    username = forms.CharField(max_length=255)
    email = forms.EmailField()
    password1 = forms.CharField(max_length=255)
    password2 = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email"]

    def __init__(self, *args, **kwargs):
        super(UsersCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Type your username ...'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Type your email ...'})
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'login-input', 'id': 'password', 'placeholder': 'Type your password...'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'login-input', 'id': 'password_confirm', 'placeholder': 'Type your password again...'})

    def clean(self):
        cleaned_data = super(UsersCreationForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.pop('password2')
        if password1 != password2:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

        return cleaned_data
