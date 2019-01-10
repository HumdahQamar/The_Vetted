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

    USER_TYPE_CHOICES = (
        (1, 'employee'),
        (2, 'admin'),
        (3, 'super_user')
    )

    type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.username

