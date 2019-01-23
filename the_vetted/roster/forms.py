from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.files.images import get_image_dimensions

from roster.models import User


class UserSignupForm(UserCreationForm):
    bio = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'bio')

    # source: https://stackoverflow.com/questions/6396442/add-image-avatar-field-to-users-in-django
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')

        try:
            # width, height = get_image_dimensions(avatar)
            #
            # max_width = max_height = 100
            # if width > max_width:
            #     raise forms.ValidationError(u'Please use an image that is %s x %s pixels or smaller.' % (max_width, max_height))

            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, GIF or PNG image.')

            if len(avatar) > (20 * 1024):
                raise forms.ValidationError(u'Avatar file size may not exceed 20k.')

        except AttributeError:
            pass

        return avatar
