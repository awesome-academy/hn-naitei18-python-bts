
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from travel.models import Profile
from django.db import models

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class ProfileForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = ('address', 'phone', 'avatar')

class SignupForm(UserCreationForm):
    address = forms.CharField(max_length = 200,required = True)
    phone = forms.CharField(max_length = 10 ,required = True)
    email = forms.EmailField(max_length=200, help_text='Required')
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
