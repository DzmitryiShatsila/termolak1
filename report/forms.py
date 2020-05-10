from django import forms
from . import models


class CasesForm(forms.ModelForm):
    class Meta:
        model = models.Cases
        fields = ('date', 'case_code', 'images', 'case', 'product', 'software',
                  'procedure', 'time', 'notes',)
        widgets = {'date': forms.SelectDateWidget}


class EmailMForm(forms.Form):
    text = forms.CharField(required=False, widget=forms.Textarea)
