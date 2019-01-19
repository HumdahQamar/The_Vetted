from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView

from roster.forms import UserSignupForm


def index(request):
    user = request.user
    if user.is_authenticated:
        return render(
            request,
            'roster/index.html',
            {
                'user': user
            }
        )
    return HttpResponse("Login pls!")


class UserSignup(FormView):
    form_class = UserSignupForm
    template_name = 'roster/user_signup.html'
    fields = ['username', 'email', 'password', 'bio']

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')
        bio = form.cleaned_data.get('bio')
        user = authenticate(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=raw_password,
            bio=bio
        )
        auth_login(self.request, user)
        return redirect('index')

