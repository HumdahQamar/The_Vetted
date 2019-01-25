from django.urls import reverse
from django.test import TestCase

from roster.models import User, Company


class UserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", email='test_user@gmail.com', password='test12345')

    def test_created_user_is_employee(self):
        self.assertIs(self.user.is_employee, True)

    def test_created_user_is_not_admin(self):
        self.assertIs(self.user.is_admin, False)

    def test_created_user_is_not_super_admin(self):
        self.assertIs(self.user.is_super_admin, False)


class HomepageViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test_user", email='test_user@gmail.com', password='test12345')

    def test_display_user_card_on_homepage(self):
        user = self.user
        self.client.login(username="test_user", password='test12345')
        response = self.client.get(reverse('home'))
        self.assertContains(response, user.username)
        self.assertContains(response, user.email)

    def test_display_new_joined_user_on_homepage(self):
        new_user = User.objects.create_user(username="new_user", email='new_user@gmail.com', password='test12345')
        self.client.login(username="test_user", password='test12345')
        response = self.client.get(reverse('home'))
        self.assertContains(response, new_user.first_name + new_user.last_name + " joined rostrr")

    def test_display_new_joined_company_on_homepage(self):
        new_company = Company.objects.create(name="Google", admin=self.user, using_roster_app=True)
        self.client.login(username="test_user", password='test12345')
        response = self.client.get(reverse('home'))
        self.assertContains(response, new_company.name + " joined rostrr")

    def test_display_new_logged_in_username_on_homepage(self):
        self.client.login(username="test_user", password='test12345')
        response = self.client.get(reverse('home'))
        self.assertContains(response, "Logged in as: " + self.user.username)

    def test_admin_can_see_manage_users_tab(self):
        user = self.user
        User.objects.filter(pk=user.pk).update(is_admin=True)
        self.client.login(username="test_user", password='test12345')
        response = self.client.get(reverse('home'))
        self.assertContains(response, "Manage Users")

    def test_employee_can_not_see_manage_users_tab(self):
        self.client.login(username="test_user", password='test12345')
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, "Manage Users")

    def test_user_can_update_profile(self):
        self.client.login(username="test_user", password='test12345')
        response = self.client.get(reverse('home'))
        self.assertContains(response, "Update Profile")


class CompanyListViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", email='test_user@gmail.com', password='test12345')
        self.company = Company.objects.create(name="Google", admin=self.user, using_roster_app=False)

    def test_list_company_on_page(self):
        self.client.login(username="test_user", password='test12345')
        response = self.client.get(reverse('browse_companies'))
        self.assertContains(response, self.company.name)

    def test_show_company_does_not_use_roster_app(self):
        self.client.login(username="test_user", password='test12345')
        response = self.client.get(reverse('browse_companies'))
        self.assertContains(response, self.company.name)
        self.assertContains(response, 'This company does not use the rostrr app')

    def test_show_company_uses_roster_app(self):
        Company.objects.filter(pk=self.company.pk).update(using_roster_app=True)
        self.client.login(username="test_user", password='test12345')
        response = self.client.get(reverse('browse_companies'))
        self.assertContains(response, self.company.name)
        self.assertNotContains(response, 'This company does not use the rostrr app')

    def test_super_admin_can_add_company(self):
        User.objects.filter(pk=self.user.pk).update(is_super_admin=True)
        self.client.login(username="test_user", password='test12345')
        response = self.client.get(reverse('browse_companies'))
        self.assertContains(response, self.company.name)
        self.assertContains(response, "Add to rostrr")

    def test_admin_can_not_add_company(self):
        self.client.login(username="test_user", password='test12345')
        response = self.client.get(reverse('browse_companies'))
        self.assertContains(response, self.company.name)
        self.assertNotContains(response, "Add to rostrr")

    def test_super_admin_can_remove_company(self):
        User.objects.filter(pk=self.user.pk).update(is_super_admin=True)
        Company.objects.filter(pk=self.company.pk).update(using_roster_app=True)
        self.client.login(username="test_user", password='test12345')
        response = self.client.get(reverse('browse_companies'))
        self.assertContains(response, self.company.name)
        self.assertContains(response, "Remove from rostrr")

    def test_admin_can_not_remove_company(self):
        Company.objects.filter(pk=self.company.pk).update(using_roster_app=True)
        self.client.login(username="test_user", password='test12345')
        response = self.client.get(reverse('browse_companies'))
        self.assertContains(response, self.company.name)
        self.assertNotContains(response, "Remove from rostrr")