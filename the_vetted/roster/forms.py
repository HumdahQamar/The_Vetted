from django import forms
from django.contrib.auth.forms import UserCreationForm

from roster.models import User


class UserSignupForm(UserCreationForm):
    bio = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'bio')
