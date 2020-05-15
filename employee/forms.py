from django.contrib.auth.models import User
from .models import Profile
from django import forms


class UserCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        widgets = {'password': forms.PasswordInput}

    hired = forms.DateField(widget=forms.SelectDateWidget)

    def clean(self):
        cd = super().clean()
        if not cd.get('first_name').isalpha() or not cd.get('last_name').isalpha():
            raise forms.ValidationError('Use only letters for name!')
        return cd


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean(self):
        cd = super().clean()
        if not cd.get('first_name').isalpha() or not cd.get('last_name').isalpha():
            raise forms.ValidationError('Use only letters for name!')
        return cd


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('hired',)

