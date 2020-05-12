from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission
from django.urls import reverse
from employee.models import Profile
import ddt


class ProfileViewTest(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.user = User.objects.create_user(username='root', password='12345')
        self.user.save()
        # self.profile = Profile.objects.create()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('employee:profile-view'))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/accounts/login/'))

    def test_view_uses_correct_template(self):
        self.client.login(username='root', password='12345')
        resp = self.client.get(reverse('employee:profile-view'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'profile.html')


@ddt.ddt
class ProfileUpdateViewTest(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.user = User.objects.create_user(username='root', password='12345')
        self.user.save()
        self.profile = Profile.objects.create(user=self.user)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('employee:profile-update'))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/accounts/login/'))

    def test_view_uses_correct_template(self):
        self.client.login(username='root', password='12345')
        resp = self.client.get(reverse('employee:profile-update'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'profile_update.html')

    def test_redirect_to_profile_view(self):
        self.client.login(username='root', password='12345')
        resp = self.client.post(
            reverse('employee:profile-update'),
            {'username': 'root', 'first_name': 'Root', 'last_name': 'Root', 'email': 'root@google.com'},)
        self.assertRedirects(resp, reverse('employee:profile-view'))

    @ddt.data('root', 'new_root')
    def test_update_username(self, username):
        self.client.login(username='root', password='12345')
        resp = self.client.post(
            reverse('employee:profile-update'),
            {'username': username, }, )
        self.assertEqual(Profile.objects.get().user.username, username)

    @ddt.data('Root', 'new_name', '')
    def test_update_first_name(self, first_name):
        self.client.login(username='root', password='12345')
        resp = self.client.post(
            reverse('employee:profile-update'),
            {'username': 'root', 'first_name': first_name,}, )
        self.assertEqual(Profile.objects.get().user.first_name, first_name)

    @ddt.data('Root', 'new_name', '')
    def test_update_last_name(self, last_name):
        self.client.login(username='root', password='12345')
        resp = self.client.post(
            reverse('employee:profile-update'),
            {'username': 'root', 'last_name': last_name, }, )
        self.assertEqual(Profile.objects.get().user.last_name, last_name)

    @ddt.data('', 'root@google.com', 'new_root@mail.ru')
    def test_update_email(self, email):
        self.client.login(username='root', password='12345')
        resp = self.client.post(
            reverse('employee:profile-update'),
            {'username': 'root', 'email': email}, )
        self.assertEqual(Profile.objects.get().user.email, email)

    @ddt.data('None', '2020-05-06', '2023-09-20')
    def test_update_hired(self, hired):
        self.client.login(username='root', password='12345')
        resp = self.client.post(
            reverse('employee:profile-update'),
            {'username': 'root', 'hired': hired}, )
        self.assertEqual(str(Profile.objects.get().hired), hired)


class ChangePasswordViewTest(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.user = User.objects.create_user(username='root', password='12345')
        self.user.save()
        self.profile = Profile.objects.create(user=self.user)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('employee:change-pass'))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/accounts/login/'))

    def test_view_uses_correct_template(self):
        self.client.login(username='root', password='12345')
        resp = self.client.get(reverse('employee:change-pass'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'change_password.html')

    def test_redirect_to_profile_view(self):
        self.client.login(username='root', password='12345')
        resp = self.client.post(
            reverse('employee:change-pass'),
            {'old_password': '12345', 'new_password1': 'qwerty', 'new_password2': 'qwerty'},)
        self.assertEqual(resp.status_code, 200)


class AllEmployeesViewTest(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='12345', is_superuser=True)
        self.user1.save()

        self.user2 = User.objects.create_user(username='user2', password='12345')
        self.user2.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('employee:all-employees'))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/accounts/login/'))

    def test_redirect_if_logged_in_but_not_permissions(self):
        self.client.login(username='user2', password='12345')
        resp = self.client.get(reverse('employee:all-employees'))
        self.assertEqual(resp.status_code, 403)

    def test_view_uses_correct_template(self):
        self.client.login(username='user1', password='12345')
        resp = self.client.get(reverse('employee:all-employees'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'all_employees.html')


class CreateEmployeeViewTest(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='12345', is_superuser=True)
        self.user1.save()

        self.user2 = User.objects.create_user(username='user2', password='12345')
        self.user2.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('employee:employee-create'))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/accounts/login/'))

    def test_redirect_if_logged_in_but_not_permissions(self):
        self.client.login(username='user2', password='12345')
        resp = self.client.get(reverse('employee:employee-create'))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/accounts/login/'))

    def test_view_uses_correct_template(self):
        self.client.login(username='user1', password='12345')
        resp = self.client.get(reverse('employee:employee-create'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'employee_create.html')

    def test_redirect_to_all_employees(self):
        self.client.login(username='user1', password='12345')
        resp = self.client.post(
            reverse('employee:employee-create'),
            {'username': 'user3', 'password': '12345', 'email': 'email@google.com', 'first_name': 'Name',
             'last_name': 'Surname', 'hired_month': 1, 'hired_day': 1, 'hired_year': 2020},)
        self.assertRedirects(resp, reverse('employee:all-employees'))
        self.assertEqual(User.objects.get(username='user3').first_name, 'Name')


class DeleteEmployeeViewTest(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='12345', is_superuser=True)
        self.user1.save()

        self.user2 = User.objects.create_user(username='user2', password='12345')
        self.user2.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('employee:employee-delete', kwargs={'username': self.user2.username}))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/accounts/login/'))

    def test_redirect_if_logged_in_but_not_permissions(self):
        self.client.login(username='user2', password='12345')
        resp = self.client.get(reverse('employee:employee-delete', kwargs={'username': self.user2.username}))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/accounts/login/'))

    def test_view_uses_correct_template(self):
        self.client.login(username='user1', password='12345')
        resp = self.client.get(reverse('employee:employee-delete', kwargs={'username': self.user2.username}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'employee_delete.html')

    def test_redirect_to_all_employees(self):
        self.client.login(username='user1', password='12345')
        resp = self.client.post(
            reverse('employee:employee-delete', kwargs={'username': self.user2.username}),
            {},)
        self.assertRedirects(resp, reverse('employee:all-employees'))

    def test_user2_deleted(self):
        self.client.login(username='user1', password='12345')
        self.assertEqual(len(User.objects.all()), 2)
        resp = self.client.post(
            reverse('employee:employee-delete', kwargs={'username': self.user2.username}),
            {}, )
        self.assertEqual(len(User.objects.all()), 1)