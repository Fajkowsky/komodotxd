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


def register(regform, data):
    data = {}
    regcd = regform.cleaned_data
    obj, created = UserData.objects.get_or_create(
        username=regcd['username'], email=regcd['email'], is_active=False)
    if created:
        mail_activation(obj, regcd)
        return HttpResponseRedirect('/thanks/')
    else:
        data['msg'] = 1
    return data


def loging(logform):
    logcd = logform.cleaned_data
    return authenticate(userID=logcd['userID'], password=logcd['password'])

def form_handle(request):
    data = {}
    regform = RegisterForm(request.POST)
    logform = LoginForm(request.POST)
    if regform.is_valid():
        data = register(regform, data)
    elif logform.is_valid():
        user = loging(logform)
        print "user:", user
        if user is not None and user.is_active:
            print login(request, user)
            data['logged'] = 1
        else:
            data['logged'] = 0
    return data

def index(request):
    data = {}
    if request.method == 'POST':
        data = form_handle(request)
    else:
        data['regform'] = RegisterForm()
        data['logform'] = LoginForm()
    return render(request, 'index.html', data)

def account(request):
    data = {}
    data['user'] = request.user.username
    print data['user']
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
