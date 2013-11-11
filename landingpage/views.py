from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core import mail
from django.template.loader import get_template
from django.template import Context
from django.contrib import auth
from django.contrib.auth import authenticate, login

from forms import RegisterForm, LoginForm
from models import UserData

connection = mail.get_connection()


def index(request, data={}):
    def form_handle(request, data={}):
        regform = RegisterForm(request.POST)
        logform = LoginForm(request.POST)

        if regform.is_valid():
            register(regform, data)

        elif logform.is_valid():
            user = loging(logform, request)

    def register(regform, data={}):
        regcd = regform.cleaned_data
        obj, created = UserData.objects.get_or_create(
            username=regcd['username'], email=regcd['email'], is_active=False)

        if created:
            mail_activation(obj, regcd)
            return HttpResponseRedirect('/thanks/')

    def loging(logform, request):
        logcd = logform.cleaned_data
        user = authenticate(userID=logcd['userID'], password=logcd['password'])

        if user is not None and user.is_active:
            login(request, user)
    # --------------------------------------------------
    if request.method == 'POST':
        data = form_handle(request)

    else:
        data['regform'] = RegisterForm()
        data['logform'] = LoginForm()

    return render(request, 'index.html', data)


def account(request, data={}):
    data['user'] = request.user.username
    return render(request, 'account.html', data)


def mail_activation(obj, cd):
    connection.open()
    html_content = get_template('email/confirmation.html').render(
        Context({'code': obj.confirmation}))
    email = mail.EmailMultiAlternatives(
        'Activation link',
        html_content,
        '',
        [cd['email']],
    )
    email.attach_alternative(html_content, "text/html")
    connection.send_messages([email])
    connection.close()


def mail_login(obj, password):
    connection.open()
    html_content = get_template('email/login.html').render(
        Context({'login': obj.userID, 'password': password}))
    email = mail.EmailMultiAlternatives(
        'LogIn',
        html_content,
        '',
        [obj.email],
    )
    email.attach_alternative(html_content, "text/html")
    connection.send_messages([email])
    connection.close()


def thanks(request):
    return render(request, 'thanks.html')


def error(request):
    return render(request, '404.html')


def confirmation(request, userid):
    obj = get_object_or_404(UserData, confirmation=userid, is_active=False)
    mail_login(obj, obj.generate_auth())
    obj.save()
    return render(request, 'confirmation.html')
