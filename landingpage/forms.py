from django import forms

from landingpage.models import UserData


class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)


class LoginForm(forms.Form):
    userID = forms.CharField(required=True)
    password = forms.CharField(required=True)


class ModifyForm(forms.Form):
    username = forms.CharField(required=False)
    email = forms.CharField(required=False)
    country = forms.CharField(required=False)
    address1 = forms.CharField(required=False)
    address2 = forms.CharField(required=False)
    telephone = forms.CharField(required=False)
    postal_code = forms.CharField(required=False)
    city = forms.CharField(required=False)
    doc_id = forms.ImageField(required=False)
    doc_vrfy = forms.ImageField(required=False)
