from django import forms
from .models import Tasks


class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ('casecode', 'deadline_time', 'deadline_date', 'author')