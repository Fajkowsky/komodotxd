from django import forms

from landingpage.models import UserData


class RegisterForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'username', 'type': 'text'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'email', 'type': 'email'}))


class LoginForm(forms.Form):
    userID = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'userID', 'type': 'text'}))
    password = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'password', 'type': 'password'}))


class ModifyForm(forms.Form):
    username = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter username', 'type': 'text'}))
    email = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter email', 'type': 'email'}))
    country = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter country', 'type': 'text'}))
    address1 = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter address 1', 'type': 'text'}))
    address2 = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter address 2', 'type': 'text'}))
    city = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter city', 'type': 'text'}))
    postal_code = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter postal code', 'type': 'text'}))
    telephone = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter telephone', 'type': 'text'}))
    doc_id = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={'class': 'btn-sm'}))
    doc_vrfy = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={'class': 'btn-sm'}))
