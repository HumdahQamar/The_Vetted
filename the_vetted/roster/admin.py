from django.contrib import admin
from .models import User, Team, Company, Invite


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'username', 'email', 'bio', 'team', 'get_type')
    search_fields = ('first_name', 'last_name', 'username')
    ordering = ('pk',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'company')
    search_fields = ('name',)
    ordering = ('pk',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'admin', 'using_roster_app')
    search_fields = ('name',)
    ordering = ('pk',)


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'company', 'timestamp')
    ordeing = ('pk',)
