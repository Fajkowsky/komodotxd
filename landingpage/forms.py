from django import forms

from landingpage.models import UserData


class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)


class LoginForm(forms.Form):
    userID = forms.CharField(required=True)
    password = forms.CharField(required=True)


class ModifyForm(forms.Form):
    country = forms.CharField(required=True)
