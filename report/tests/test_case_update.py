from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from report.models import Cases
import ddt


@ddt.ddt
class CaseUpdateViewTest(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.user = User.objects.create_user(username='root', password='qwerty')
        self.user.save()
        self.test_case = Cases.objects.create(date='2020-05-06', author=self.user, case_code='qwerty', images='ct',
                                              case='s', product='knee', software='mimics', procedure='rec', time=60)
        self.test_case.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('report:case-update', kwargs={'slug': self.test_case.id, }))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/accounts/login/'))

    def test_view_uses_correct_template(self):
        self.client.login(username='root', password='qwerty')
        resp = self.client.get(reverse('report:case-update', kwargs={'slug': self.test_case.id, }))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'report/case_update.html')

    def test_redirect_to_all_cases(self):
        self.client.login(username='root', password='qwerty')
        resp = self.client.post(
            reverse('report:case-update', kwargs={'slug': self.test_case.id, }),
            {'date': '2020-05-06', 'case_code': '12345', 'images': 'ct', 'case': 's', 'product': 'knee',
             'software': 'mimics', 'procedure': 'check', 'time': '55'},
        )
        self.assertRedirects(resp, reverse('report:all-cases'))

    def test_update_date(self):
        self.client.login(username='root', password='qwerty')
        resp = self.client.get(reverse('report:case-update', kwargs={'slug': self.test_case.id, }))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(
            reverse('report:case-update', kwargs={'slug': self.test_case.id, }),
            {'date': '2019-05-06', 'case_code': 'qwerty', 'images': 'ct', 'case': 's', 'product': 'knee',
             'software': 'mimics', 'procedure': 'rec', 'time': '60'},)
        case = Cases.objects.get()
        self.assertEqual(str(case.date), '2019-05-06')

    @ddt.data('new_case_code')
    def test_update_case_code(self, case_code):
        self.client.login(username='root', password='qwerty')
        resp = self.client.get(reverse('report:case-update', kwargs={'slug': self.test_case.id, }))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(
            reverse('report:case-update', kwargs={'slug': self.test_case.id, }),
            {'date': '2020-05-06', 'case_code': case_code, 'images': 'ct', 'case': 's', 'product': 'knee',
             'software': 'mimics', 'procedure': 'rec', 'time': '60'},)
        case = Cases.objects.get()
        self.assertEqual(case.case_code, case_code)

    @ddt.data('ct', 'mri')
    def test_update_images(self, images):
        self.client.login(username='root', password='qwerty')
        resp = self.client.get(reverse('report:case-update', kwargs={'slug': self.test_case.id, }))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(
            reverse('report:case-update', kwargs={'slug': self.test_case.id, }),
            {'date': '2020-05-06', 'case_code': 'qwerty', 'images': images, 'case': 's', 'product': 'knee',
             'software': 'mimics', 'procedure': 'rec', 'time': '60'},)
        case = Cases.objects.get()
        self.assertEqual(case.images, images)

    @ddt.data('s', 'o')
    def test_update_case(self, test_case):
        self.client.login(username='root', password='qwerty')
        resp = self.client.get(reverse('report:case-update', kwargs={'slug': self.test_case.id, }))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(
            reverse('report:case-update', kwargs={'slug': self.test_case.id, }),
            {'date': '2020-05-06', 'case_code': 'qwerty123', 'images': 'ct', 'case': test_case, 'product': 'knee',
             'software': 'mimics', 'procedure': 'rec', 'time': '60'}, )
        case = Cases.objects.get()
        self.assertEqual(case.case, test_case)

    @ddt.data('spine', 'knee', 'hip', 'shoulder', 'forearm', 'wrist', 'ankle', )
    def test_update_product(self, product):
        self.client.login(username='root', password='qwerty')
        resp = self.client.get(reverse('report:case-update', kwargs={'slug': self.test_case.id, }))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(
            reverse('report:case-update', kwargs={'slug': self.test_case.id, }),
            {'date': '2020-05-06', 'case_code': 'qwerty123', 'images': 'ct', 'case': 's', 'product': product,
             'software': 'mimics', 'procedure': 'rec', 'time': '60'}, )
        case = Cases.objects.get()
        self.assertEqual(case.product, product)

    @ddt.data('mimics', 'avizo')
    def test_update_software(self, software):
        self.client.login(username='root', password='qwerty')
        resp = self.client.get(reverse('report:case-update', kwargs={'slug': self.test_case.id, }))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(
            reverse('report:case-update', kwargs={'slug': self.test_case.id, }),
            {'date': '2020-05-06', 'case_code': 'qwerty123', 'images': 'ct', 'case': 's', 'product': 'knee',
             'software': software, 'procedure': 'rec', 'time': '60'}, )
        case = Cases.objects.get()
        self.assertEqual(case.software, software)

    @ddt.data('rec', 'check')
    def test_update_procedure(self, procedure):
        self.client.login(username='root', password='qwerty')
        resp = self.client.get(reverse('report:case-update', kwargs={'slug': self.test_case.id, }))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(
            reverse('report:case-update', kwargs={'slug': self.test_case.id, }),
            {'date': '2020-05-06', 'case_code': 'qwerty123', 'images': 'ct', 'case': 's', 'product': 'knee',
             'software': 'mimics', 'procedure': procedure, 'time': '60'}, )
        case = Cases.objects.get()
        self.assertEqual(case.procedure, procedure)

    @ddt.data(25, 35)
    def test_update_time(self, time):
        self.client.login(username='root', password='qwerty')
        resp = self.client.get(reverse('report:case-update', kwargs={'slug': self.test_case.id, }))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(
            reverse('report:case-update', kwargs={'slug': self.test_case.id, }),
            {'date': '2020-05-06', 'case_code': 'qwerty123', 'images': 'ct', 'case': 's', 'product': 'knee',
             'software': 'mimics', 'procedure': 'rec', 'time': time}, )
        case = Cases.objects.get()
        self.assertEqual(case.time, time)
