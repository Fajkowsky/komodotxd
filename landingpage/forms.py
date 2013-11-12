from django import forms

from landingpage.models import UserData


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()


class LoginForm(forms.Form):
    userID = forms.CharField()
    password = forms.CharField()


class ModifyForm(forms.Form):
    country = forms.CharField(required=True)
