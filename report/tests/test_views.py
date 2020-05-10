from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from report.models import Cases


class CaseDeleteViewTest(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.user = User.objects.create_user(username='root', password='12345')
        self.user.save()
        for _ in range(15):
            self.test_case = Cases.objects.create(date='2020-05-06', author=self.user, case_code='qwerty', images='ct',
                                                  case='s', product='knee', software='mimics', procedure='rec',
                                                  time=60)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('report:case-delete', kwargs={'slug': self.test_case.id, }))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/accounts/login/'))

    def test_view_uses_correct_template(self):
        self.client.login(username='root', password='12345')
        resp = self.client.get(reverse('report:case-delete', kwargs={'slug': self.test_case.id, }))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'report/case_delete.html')

    def test_redirect_to_all_cases(self):
        self.client.login(username='root', password='12345')
        resp = self.client.post(
            reverse('report:case-delete', kwargs={'slug': self.test_case.id, }),
            {},)
        self.assertRedirects(resp, reverse('report:all-cases'))

    def test_case_deleted(self):
        self.client.login(username='root', password='12345')
        resp = self.client.post(
            reverse('report:case-delete', kwargs={'slug': self.test_case.id, }),
            {}, )
        self.assertTrue(len(Cases.objects.all()) == 14)


class SearchResultsViewTest(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.user = User.objects.create_user(username='root', password='12345')
        self.user.save()
        self.test_case1 = Cases.objects.create(date='2020-05-06', author=self.user, case_code='qwerty', images='ct',
                                               case='s', product='knee', software='mimics', procedure='rec',
                                               time=60)
        self.test_case2 = Cases.objects.create(date='2020-05-06', author=self.user, case_code='swerty', images='ct',
                                               case='s', product='knee', software='mimics', procedure='rec',
                                               time=60)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('report:search-results'))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/accounts/login/'))

    def test_view_uses_correct_template(self):
        self.client.login(username='root', password='12345')
        resp = self.client.get(reverse('report:search-results'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'report/search_results.html')

    def test_search_results_are_correct(self):
        self.client.login(username='root', password='12345')
        resp = self.client.get('/search_results/?q=qwerty')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['object_list']), 1)
        resp = self.client.get('/search_results/?q=werty')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['object_list']), 2)
        resp = self.client.get('/search_results/?q=123')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['object_list']), 0)
