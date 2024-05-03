from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth.models import User

from django import forms

from .models import *

from django.forms.widgets import PasswordInput, TextInput


class CreateUserForm(UserCreationForm):
    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

    def get_error_message(self):
        errors = self.errors.get_json_data()
        return errors


class VehicleForm(forms.ModelForm):
    class Meta:

        model = Vehicle
        fields = '__all__'
