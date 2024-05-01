from django.contrib.auth.forms import AuthenticationForm
from django import forms

from django.forms.widgets import PasswordInput, TextInput


# Login form

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
    
