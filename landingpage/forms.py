from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(required=False)
