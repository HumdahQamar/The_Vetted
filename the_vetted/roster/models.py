from django.db import models
from django.contrib.auth.models import AbstractUser


class Company(models.Model):
    name = models.CharField(max_length=20)
    admin = models.OneToOneField('User', related_name='admin', on_delete=models.SET_NULL, null=True)
    using_roster_app = models.BooleanField(default=False)
    logo = models.ImageField(upload_to='logos/', blank=True)
    joined_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=20)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class User(AbstractUser):
    bio = models.CharField(max_length=200)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    is_employee = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_super_admin = models.BooleanField(default=False)
    # joined_at = models.DateField(auto_now_add=True)
    company = models.ForeignKey(
        Company,
        related_name='user_company',
        on_delete=models.SET_NULL,
        null=True,
        unique=False
    )
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    def __str__(self):
        return self.username

    def get_type(self):
        user_type = []

        if self.is_employee:
            user_type.append('Employee')
        if self.is_admin:
            user_type.append('Admin')
        if self.is_super_admin:
            user_type.append('Super Admin')

        return ','.join(user_type)

    get_type.short_description = 'User Type'


class Invite(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name='company', on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now_add=True)
    message = models.CharField(max_length=500)
    status = models.CharField(max_length=20, default='Inactive')


class Request(models.Model):
    sender = models.ForeignKey(User, related_name='requet_sender', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name='request_company', on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Inactive')