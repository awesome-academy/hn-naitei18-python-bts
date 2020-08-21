
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from travel.models import Profile
from django.db import models

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('address', 'phone')

class SignUpForm(UserCreationForm):
    address = forms.CharField(max_length = 200,required = True)
    phone = forms.CharField(max_length = 10 ,required = True)
    username = forms.CharField(max_length = 100, required = True)
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        # help_text=password_validation.password_validators_help_text_html(),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'address','phone', 'password1', 'password2', )
