from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.list import ListView

from roster.forms import UserSignupForm
from roster.models import User, Company, Team


# def index(request):
#     user = request.user
#     if user.is_authenticated:
#         return render(
#             request,
#             'roster/index.html',
#             {
#                 'user': user
#             }
#         )
#     return HttpResponse("Login pls!")


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
        return redirect('homepage')


class HomePage(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        return render(
            request,
            'roster/homepage.html',
            {
                'user': request.user
            }
        )


class Settings(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return render(
                request,
                'roster/settings_basic.html',
                {
                    'user': user
                }
            )


class UpdateProfile(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'bio']
    pk_url_kwarg = 'pk'
    template_name = 'roster/update_profile.html'
    success_url = reverse_lazy('settings')  # change to some page that displays user info

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class CompanyList(ListView):
    model = Company
    template_name = 'roster/company_list.html'

    # def get_context_data(self, *, object_list=None, **kwargs):
    def get_queryset(self):
        return Company.objects.order_by('name')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # context['user'] = self.request.user
    #     context['companies'] = Company.objects.order_by('name')


def company_add(request, pk):
    Company.objects.filter(pk=pk).update(using_roster_app=True)
    return redirect('browse_companies')


def company_remove(request, pk):
    Company.objects.filter(pk=pk).update(using_roster_app=False)
    return redirect('browse_companies')


class CompanyDetails(DetailView):
    model = Company
    pk_url_kwarg = 'pk'
    template_name = 'roster/company_details.html'

    def get_context_data(self, **kwargs):
        company = Company.objects.get(pk=self.kwargs.get('pk'))
        context = super().get_context_data(**kwargs)
        context['teams'] = Team.objects.filter(company=company).order_by('name')
        context['employees'] = User.objects.filter(company=company).order_by('team', 'first_name')
        return context
        # employees = []
        # for team in list(context.get('teams')):

        # context['employees'] = User.objects.filter(company=company).order_by('name')
        # context[]


