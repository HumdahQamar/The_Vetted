from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic.edit import CreateView, FormView, UpdateView

from roster.forms import UserSignupForm
from roster.models import User


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


class LandingPage(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        return render(
            request,
            'roster/landing_page.html',
            {
                'user': request.user
            }
        )


class Settings(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            if user.is_superuser:
                return render(
                    request,
                    'roster/settings_super_admin.html',
                    {
                        'user': user
                    }
                )
            elif user.is_staff:
                return render(
                    request,
                    'roster/settings_admin.html',
                    {
                        'user': user
                    }
                )
            else:
                return render(
                    request,
                    'roster/settings_basic.html',
                    {
                        'user': user
                    }
                )


class UpdateProfile(UpdateView):
    model = User
    fields = ['email']
    pk_url_kwarg = 'pk'
    template_name = 'roster/update_profile.html'

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)