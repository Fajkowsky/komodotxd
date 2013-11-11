from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()


class LoginForm(forms.Form):
    userID = forms.CharField()
    password = forms.CharField()
