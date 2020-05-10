from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from report.models import Cases
import ddt


@ddt.ddt
class FilterCasesViewTest(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.user = User.objects.create_user(username='root', password='12345')
        self.user.save()
        self.test_case1 = Cases.objects.create(date='2020-05-06', author=self.user, case_code='test1', images='ct',
                                               case='o', product='knee', software='avizo', procedure='rec',
                                               time=60)
        self.test_case2 = Cases.objects.create(date='2020-05-06', author=self.user, case_code='test2', images='ct',
                                               case='s', product='hip', software='mimics', procedure='rec',
                                               time=60)
        self.test_case3 = Cases.objects.create(date='2020-05-07', author=self.user, case_code='test3', images='ct',
                                               case='s', product='spine', software='avizo', procedure='check',
                                               time=60)
        self.test_case4 = Cases.objects.create(date='2019-05-06', author=self.user, case_code='test4', images='mri',
                                               case='s', product='shoulder', software='mimics', procedure='check',
                                               time=60)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('report:case-filter'))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/accounts/login/'))

    def test_view_uses_correct_template(self):
        self.client.login(username='root', password='12345')
        resp = self.client.get(reverse('report:case-filter'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'report/case_filter.html')

    @ddt.data(('2020-05-06', 2),
              ('', 4))
    @ddt.unpack
    def test_filter_by_date(self, date, expected):
        self.client.login(username='root', password='12345')
        resp = self.client.get(
            reverse('report:case-filter'),
            {'date': date, })
        self.assertEqual(len(resp.context['filter'].qs), expected)

    @ddt.data(('ct', 3),
              ('mri', 1),
              ('', 4))
    @ddt.unpack
    def test_filter_by_images(self, images, expected):
        self.client.login(username='root', password='12345')
        resp = self.client.get(
            reverse('report:case-filter'),
            {'images': images, })
        self.assertEqual(len(resp.context['filter'].qs), expected)

    @ddt.data(('s', 3),
              ('o', 1),
              ('', 4))
    @ddt.unpack
    def test_filter_by_case(self, case, expected):
        self.client.login(username='root', password='12345')
        resp = self.client.get(
            reverse('report:case-filter'),
            {'case': case, })
        self.assertEqual(len(resp.context['filter'].qs), expected)

    @ddt.data(('mimics', 2),
              ('avizo', 2),
              ('', 4))
    @ddt.unpack
    def test_filter_by_software(self, software, expected):
        self.client.login(username='root', password='12345')
        resp = self.client.get(
            reverse('report:case-filter'),
            {'software': software, })
        self.assertEqual(len(resp.context['filter'].qs), expected)

    @ddt.data(('spine', 1),
              ('knee', 1),
              ('hip', 1),
              ('shoulder', 1),
              ('forearm', 0),
              ('wrist', 0),
              ('ankle', 0),
              ('', 4))
    @ddt.unpack
    def test_filter_by_product(self, product, expected):
        self.client.login(username='root', password='12345')
        resp = self.client.get(
            reverse('report:case-filter'),
            {'product': product, })
        self.assertEqual(len(resp.context['filter'].qs), expected)

    @ddt.data(('rec', 2),
              ('check', 2),
              ('', 4))
    @ddt.unpack
    def test_filter_by_procedure(self, procedure, expected):
        self.client.login(username='root', password='12345')
        resp = self.client.get(
            reverse('report:case-filter'),
            {'procedure': procedure, })
        self.assertEqual(len(resp.context['filter'].qs), expected)
