from django.shortcuts import render
from django.utils import timezone
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from .models import Cases
from . import forms
from django.core.mail import EmailMessage
from .filters import CasesFilter
import requests



# Create your views here.


class TasksView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'report/tasks.html'


class MyCases(LoginRequiredMixin, generic.CreateView, generic.list.MultipleObjectMixin):
    form_class = forms.CasesForm
    success_url = '/'
    template_name = 'report/all_cases.html'
    context_object_name = 'form'
    paginate_by = 15

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        object_list = Cases.objects.filter(author=self.request.user)
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


class CaseUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Cases
    fields = ('date', 'case_code', 'images', 'case', 'product', 'software', 'procedure', 'time',)
    template_name = 'report/case_update.html'
    success_url = reverse_lazy('report:all-cases')
    slug_field = 'id'


class CaseDelete(LoginRequiredMixin, generic.DeleteView):
    model = Cases
    template_name = 'report/case_delete.html'
    slug_field = 'id'
    success_url = reverse_lazy('report:all-cases')


@login_required()
def sent_email(request):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxd8899fbc202f43ab94b96befef7a0e8d.mailgun.org/messages",
        auth=("api", "0c3f745014cd6d362ac8af133916042b-3e51f8d2-0de22ca2"),
        data={"from": "Excited User <mailgun@andboxd8899fbc202f43ab94b96befef7a0e8d.mailgun.org>",
              "to": ["bar@example.com", "andboxd8899fbc202f43ab94b96befef7a0e8d.mailgun.org"],
              "subject": "Hello",
              "text": "Testing some Mailgun awesomness!"})

# @login_required()
# def sent_email(request):
#     cases = Cases.objects.filter(date=timezone.now()).filter(
#         author=request.user)
#     ct_knee = Cases.get_detail('ct', 's', 'knee', 'mimics', 'rec').filter(
#         date=timezone.now()).filter(author=request.user)
#     ct_knee_avizo = Cases.get_detail('ct', 's', 'knee', 'avizo', 'rec').filter(
#         date=timezone.now()).filter(author=request.user)
#     ct_hip = Cases.get_detail('ct', 's', 'hip', 'mimics', 'rec').filter(
#         date=timezone.now()).filter(author=request.user)
#     ct_shoulder = Cases.get_detail('ct', 's', 'shoulder', 'mimics',
#                                    'rec').filter(date=timezone.now()).filter(
#         author=request.user)
#     ct_spine = Cases.get_detail(r'ct', 's', 'spine', 'mimics', 'rec').filter(
#         date=timezone.now()).filter(author=request.user)
#     mri_knee = Cases.get_detail('mri', 's', 'knee', 'mimics', 'rec').filter(
#         date=timezone.now()).filter(author=request.user)
#     ct_knee_check = Cases.get_detail('ct', 's', 'knee', 'mimics',
#                                      'check').filter(
#         date=timezone.now()).filter(author=request.user)
#     ct_hip_check = Cases.get_detail('ct', 's', 'hip', 'mimics', 'check').filter(
#         date=timezone.now()).filter(author=request.user)
#     ct_shoulder_check = Cases.get_detail('ct', 's', 'shoulder', 'mimics',
#                                          'check').filter(
#         date=timezone.now()).filter(author=request.user)
#     osteotomy = cases.filter(case='o')
#     sent = False
#     if request.method == "POST":
#         form = forms.EmailMForm(request.POST)
#
#         if form.is_valid():
#             cd = form.cleaned_data
#             body = cd['text']
#             subject = cd['subject']
#             email = EmailMessage(subject, body, request.user.email, ['root@google.com'])
#             email = EmailMessage(subject, body, request.user.email, ['rosas30398@beiop.com'])
#             email.send()
#             sent = True
#     else:
#         form = forms.EmailMForm()
#     return render(request,
#                   'report/sent_email.html',
#                   {'cases': cases,
#                    'ct_knee': ct_knee,
#                    'ct_knee_avizo': ct_knee_avizo,
#                    'ct_hip': ct_hip,
#                    'ct_shoulder': ct_shoulder,
#                    'ct_spine': ct_spine,
#                    'mri_knee': mri_knee,
#                    'ct_knee_check': ct_knee_check,
#                    'ct_hip_check': ct_hip_check,
#                    'ct_shoulder_check': ct_shoulder_check,
#                    'osteotomy': osteotomy,
#                    'form': form,
#                    'sent': sent})


class SearchResultsView(LoginRequiredMixin, generic.ListView):
    model = Cases
    template_name = 'report/search_results.html'
    context_object_name = 'cases'

    def get_queryset(self):
        query = ''
        if self.request.GET.get('q'):
            query = self.request.GET.get('q')
        object_list = Cases.objects.filter(case_code__icontains=query)
        return object_list


class FilterCasesView(LoginRequiredMixin, generic.ListView):
    model = Cases
    template_name = 'report/case_filter.html'
    context_object_name = 'filtered_cases'

    def get_queryset(self):
        queryset = Cases.objects.filter(author=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = CasesFilter(self.request.GET, queryset=self.get_queryset())
        return context
