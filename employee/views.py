from django.shortcuts import render
from . import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views import generic
from django.contrib.auth.models import User
from .models import Profile
from report.models import Cases
from django.urls import reverse
from django.db.models import Avg


# Create your views here.


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'profile.html'


@login_required
def profile_update(request):
    if request.method == 'POST':
        user_form = forms.UserUpdateForm(instance=request.user,
                                         data=request.POST)
        profile_form = forms.ProfileUpdateForm(instance=request.user.profile,
                                               data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(reverse('employee:profile-view'))
    else:
        user_form = forms.UserUpdateForm(instance=request.user)
        profile_form = forms.ProfileUpdateForm(instance=request.user.profile)
    return render(request,
                  'profile_update.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return render(request,
                          'change_password_done.html',
                          {'form': form})
    else:
        form = PasswordChangeForm(request.user)
    return render(request,
                  'change_password.html',
                  {'form': form})


@login_required
@permission_required('')
def crate_employee(request):
    if request.method == 'POST':
        user_form = forms.UserCreateForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            Profile.objects.create(user=new_user, hired=user_form.cleaned_data['hired'])
            return redirect(reverse('employee:all-employees'))
    else:
        user_form = forms.UserCreateForm()
    return render(request,
                  'employee_create.html',
                  {'user_form': user_form})


@login_required
@permission_required('')
def delete_employee(request, username):
    employee = User.objects.get(username=username)
    if request.method == 'POST':
        employee.delete()
        return redirect(reverse('employee:all-employees'))
    return render(request,
                  'employee_delete.html',
                  {'employee': employee})


class AllEmployees(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = ''
    model = User
    template_name = 'all_employees.html'
    context_object_name = 'users'


class EmployeeDetail(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    permission_required = ''
    model = User
    slug_field = 'username'
    template_name = 'employee_detail.html'
    context_object_name = 'employee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cases'] = Cases.objects.filter(author__username=context['employee'])[:30]
        context['ct_knee_rec'] = Cases.get_detail('ct', 's', 'knee', 'mimics', 'rec').filter(
            author__username=context['employee']).aggregate(Avg('time'))['time__avg']
        context['mri_knee_rec'] = Cases.get_detail('mri', 's', 'knee', 'mimics', 'rec').filter(
            author__username=context['employee']).aggregate(Avg('time'))['time__avg']
        context['ct_hip_rec'] = Cases.get_detail('ct', 's', 'hip', 'mimics', 'rec').filter(
            author__username=context['employee']).aggregate(Avg('time'))['time__avg']
        context['ct_shoulder_rec'] = Cases.get_detail('ct', 's', 'shoulder', 'mimics', 'rec').filter(
            author__username=context['employee']).aggregate(Avg('time'))['time__avg']
        context['ct_spine_rec'] = Cases.get_detail('ct', 's', 'spine', 'mimics', 'rec').filter(
            author__username=context['employee']).aggregate(Avg('time'))['time__avg']
        context['osteo'] = Cases.get_detail('ct', 'o', '', 'mimics', 'rec').filter(
            author__username=context['employee']).aggregate(Avg('time'))['time__avg']
        context['ct_knee_check'] = Cases.get_detail('ct', 's', 'knee', 'mimics', 'check').filter(
            author__username=context['employee']).aggregate(Avg('time'))['time__avg']
        context['ct_hip_check'] = Cases.get_detail('ct', 's', 'hip', 'mimics', 'check').filter(
            author__username=context['employee']).aggregate(Avg('time'))['time__avg']
        context['ct_shoulder_check'] = Cases.get_detail('ct', 's', 'shoulder', 'mimics', 'check').filter(
            author__username=context['employee']).aggregate(Avg('time'))['time__avg']
        return context
