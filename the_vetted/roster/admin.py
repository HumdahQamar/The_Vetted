from django.contrib import admin
from .models import User, Team, Company


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'bio', 'team', 'get_type')
    search_fields = ('first_name', 'last_name', 'username')
    ordering = ('pk',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'company')
    search_fields = ('name',)
    ordering = ('pk',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)
    ordering = ('pk',)
