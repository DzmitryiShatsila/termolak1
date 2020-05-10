from django.contrib.auth.models import User
from .models import Profile
from django import forms


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        widgets = {'password': forms.PasswordInput}

    hired = forms.DateField(widget=forms.SelectDateWidget)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('hired',)
        widgets = {'hired': forms.SelectDateWidget}


class UserDeleteForm(forms.Form):
    pass
