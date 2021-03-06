from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.list import ListView

from roster.forms import UserSignupForm
from roster.models import User, Company, Team, Invite, Request


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
            bio=bio,
            is_employee=True
        )
        auth_login(self.request, user)
        return redirect('home')


class HomePage(LoginRequiredMixin, ListView):
    model = User
    login_url = reverse_lazy('login')
    template_name = 'roster/homepage.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['user'] = user
        context['new_to_roster_user'] = User.objects.order_by('-date_joined').exclude(pk=user.pk)[:5]
        context['new_to_roster_company'] = Company.objects.order_by('-joined_at')[:5]
        return context


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
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class CompanyList(ListView):
    model = Company
    template_name = 'roster/company_list.html'

    def get_queryset(self):
        return Company.objects.order_by('name')


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


def add_user_to_company(request, user_pk, company_pk):
    company = Company.objects.get(pk=company_pk)
    User.objects.filter(pk=user_pk).update(company=company)
    return redirect('home')


def remove_user_from_company(request, pk):
    User.objects.filter(pk=pk).update(company=None, team=None)
    return redirect('home')


class UserList(ListView):
    model = User
    template_name = 'roster/user_list.html'

    def get_queryset(self):
        return User.objects.order_by('first_name')


def send_invite(request, receiver_pk, sender_pk, company_pk):
    receiver = User.objects.get(pk=receiver_pk)
    sender = User.objects.get(pk=sender_pk)
    company = Company.objects.get(pk=company_pk)
    status = "Active"
    invite = Invite(sender=sender, receiver=receiver, company=company, status=status)
    invite.save()
    return redirect('manage_users')


class InviteList(ListView):
    model = Invite
    template_name = 'roster/invites_list.html'

    def get_queryset(self):
        return Invite.objects.filter(receiver=self.request.user).order_by('-timestamp')


def accept_invite(request, invite_pk):
    invite = Invite.objects.get(pk=invite_pk)
    User.objects.filter(pk=request.user.pk).update(company=invite.company)
    invite.delete()
    return redirect('manage_users')


def reject_invite(request, invite_pk):
    invite = Invite.objects.get(pk=invite_pk)
    invite.delete()
    return redirect('manage_users')


class RequestList(ListView):
    model = Request
    template_name = 'roster/requests_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Request.objects.filter(company=user.company, status='Active').order_by('-timestamp')
        elif user.is_employee:
            return Request.objects.filter(sender=user).order_by('-timestamp')


def send_request(request, sender_pk, company_pk):
    sender = User.objects.get(pk=sender_pk)
    company = Company.objects.get(pk=company_pk)
    status = "Active"
    request_object = Request(sender=sender, company=company, status=status)
    request_object.save()
    return redirect('request_list')


def accept_request(request, request_pk):
    request_object = Request.objects.get(pk=request_pk)
    User.objects.filter(pk=request_object.sender.pk).update(company=request_object.company)
    Request.objects.filter(pk=request_object.pk).update(status='Accepted')
    return redirect('request_list')


def reject_request(request, request_pk):
    Request.objects.filter(pk=request_pk).update(status='Rejected')
    return redirect('request_list')


def delete_request(request, request_pk):
    request_object = Request.objects.get(pk=request_pk)
    request_object.delete()
    return redirect('request_list')