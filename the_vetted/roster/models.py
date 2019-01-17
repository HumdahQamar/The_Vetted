from django.db import models
from django.contrib.auth.models import AbstractUser


class Company(models.Model):
    name = models.CharField(max_length=20)

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
    is_employee = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_super_admin = models.BooleanField(default=False)

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