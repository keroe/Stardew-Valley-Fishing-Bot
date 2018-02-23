from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=False, help_text='Optional. No emails will be sent, this is only to change your password if you forget it.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )