from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views import generic
from .models import Tasks
from . import forms
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
# Create your views here.


@login_required
@permission_required('')
def task_done(request, id):
    if request.method == 'GET':
        task = Tasks.objects.get(id=id)
        task.status = 'd'
        task.save()
        if len(Tasks.objects.filter(status='d')) > 10:
            Tasks.objects.filter(status='d')[9].delete()
        return redirect(reverse('tasks:all-tasks'))


@login_required
@permission_required('')
def task_move_back(request, id):
    if request.method == 'GET':
        task = Tasks.objects.get(id=id)
        task.status = 'r'
        task.save()
        return redirect(reverse('tasks:all-tasks'))


class AllTasks(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = ''
    model = Tasks
    form_class = forms.TaskForm
    template_name = 'all_tasks.html'
    context_object_name = 'form'
    success_url = reverse_lazy('tasks:all-tasks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['tasks'] = Tasks.objects.all()
        return context


class TaskUpdate(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    permission_required = ''
    model = Tasks
    form_class = forms.TaskForm
    success_url = reverse_lazy('tasks:all-tasks')
    context_object_name = 'task'
    template_name = 'task_detail.html'
    slug_field = 'id'


class TaskDelete(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    permission_required = ''
    model = Tasks
    context_object_name = 'task'
    success_url = reverse_lazy('tasks:all-tasks')
    slug_field = 'id'
    template_name = 'task_delete.html'
