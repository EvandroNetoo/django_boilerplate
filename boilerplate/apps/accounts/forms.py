from django import forms
from django.contrib.auth.forms import AuthenticationForm, BaseUserCreationForm

from accounts.models import User


class SignupForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data['email']
        return email.lower()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autofocus'] = True

        for field in self.fields:
            self.fields[field].required = True


class SigninForm(AuthenticationForm):
    def get_invalid_login_error(self):
        return forms.ValidationError(
            'Credenciais inválidas.',
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        return username.lower()
