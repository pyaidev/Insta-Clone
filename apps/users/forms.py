from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email"]

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'login-input',
                'placeholder': 'Type your username...',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'login-input',
                'placeholder': 'Type your email...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput \
            (attrs={'class': 'login-input', 'id': 'password', 'placeholder': 'Type your password...'})
        self.fields['password2'].widget = forms.PasswordInput \
            (attrs={'class': 'login-input', 'id': 'password_confirm', 'placeholder': 'Type your password again...'})

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            return user
