from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from report.models import Cases


class MyCasesViewTest(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.user = User.objects.create_user(username='root', password='12345')
        self.user.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('report:all-cases'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/accounts/login/?next=/')

    def test_view_uses_correct_template(self):
        self.client.login(username='root', password='12345')
        resp = self.client.get(reverse('report:all-cases'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'report/all_cases.html')

    def test_created_one_case(self):
        self.client.login(username='root', password='12345')
        resp = self.client.post(
            '/',
            {'date': '2020-05-06',
             'case_code': '12345',
             'images': 'ct',
             'case': 's',
             'product': 'knee',
             'software': 'mimics',
             'procedure': 'check',
             'time': '55'},
        )
        mat = Cases.objects.get()
        self.assertEqual(mat.case_code, '12345')


class PaginationTest(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.user = User.objects.create_user(username='root', password='12345')
        self.user.save()
        for _ in range(20):
            Cases.objects.create(date='2020-05-06', author=self.user, case_code='111', images='ct', case='s',
                                 product='knee', software='mimics', procedure='rec', time='55')

    def test_pagination_is_15(self):
        self.client.login(username='root', password='12345')
        resp = self.client.get(reverse('report:all-cases'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(len(resp.context['object_list']) == 15)
        resp = self.client.get(reverse('report:all-cases')+'?page=2')
        self.assertTrue(len(resp.context['object_list']) == 5)
