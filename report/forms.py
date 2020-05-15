from django import forms
from . import models
from django.utils import timezone, dateformat


class CasesForm(forms.ModelForm):
    class Meta:
        model = models.Cases
        fields = ('date', 'case_code', 'images', 'case', 'product', 'software',
                  'procedure', 'time', 'notes',)
        widgets = {'date': forms.SelectDateWidget}


class EmailMForm(forms.Form):
    to_email = forms.EmailField(initial='django.tests.dzmitryi@gmail.com')
    subject = forms.CharField(initial=dateformat.format(timezone.now().date(), 'd M Y'))
    text = forms.CharField(required=False, widget=forms.Textarea)
