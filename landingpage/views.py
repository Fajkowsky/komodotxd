from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.mail import send_mail

from forms import RegisterForm


def index(request):
    data = {}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # User.objects.create_user(username=cd['username'], email=cd['email'])
            send_mail('Registration', 'Here is the message.', 'from@example.com', [cd['email']])
            return HttpResponseRedirect('/thanks/')
    else:
        data['form'] = RegisterForm()
    return render(request, 'index.html', data)


def thanks(request):
    return render(request, 'thanks.html')
