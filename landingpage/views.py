from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.core import mail
from django.template.loader import get_template
from django.template import Context
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from forms import RegisterForm, LoginForm, ModifyForm
from models import UserData

connection = mail.get_connection()


def index(request, data={}):
    def handleforms(request):
        logging = loging(request)
        registering = register(request)
        if logging:
            return logging
        elif registering:
            return registering
        else:
            return False

    def register(request):
        regform = RegisterForm(request.POST)

        if regform.is_valid():
            regcd = regform.cleaned_data
            obj, created = UserData.objects.get_or_create(
                username=regcd['username'], email=regcd['email'], is_active=False)

            if created:
                mail_activation(obj, regcd)

            return HttpResponseRedirect('/thanks/')

    def loging(request):
        logform = LoginForm(request.POST)

        if logform.is_valid():
            logcd = logform.cleaned_data
            user = authenticate(
                userID=logcd['userID'], password=logcd['password'])

            if user is not None and user.is_active:
                login(request, user)

            return HttpResponseRedirect('/account/')

    def create_forms(data={}):
        data['regform'] = RegisterForm()
        data['logform'] = LoginForm()
        return data
    # --------------------------------------------------
    if not request.user.is_authenticated():
        data.update(create_forms())
        data['user'] = '-'

    if request.method == 'POST':
        forms_response = handleforms(request)
        if forms_response:
            return forms_response

    data.update(create_forms())

    return render(request, 'index.html', data)


@login_required
def account(request, data={}):
    data['user'] = request.user
    return render(request, 'account.html', data)


@login_required
def modify(request, data={}):
    def prepare_data():
        data['user'] = request.user
        data['form'] = ModifyForm()
        return data
    # --------------------------------------------------
    if request.method == 'POST':
        form = ModifyForm(request.POST)
        logedUser = request.user
        if form.is_valid():
            cd = form.cleaned_data
            UserData.objects.filter(
                pk=logedUser.id).update(country=cd['country'])
    data.update(prepare_data())
    return render(request, 'modify.html', data)


def logouting(request):
    logout(request)
    return HttpResponseRedirect('/')


def mail_activation(obj, cd):
    connection.open()
    html_content = get_template('email/confirmation.html').render(
        Context({'code': obj.confirmation}))
    email = mail.EmailMultiAlternatives(
        'Activation link', html_content, '', [cd['email']], )
    email.attach_alternative(html_content, "text/html")
    connection.send_messages([email])
    connection.close()


def mail_login(obj, password):
    connection.open()
    html_content = get_template('email/login.html').render(
        Context({'login': obj.userID, 'password': password}))
    email = mail.EmailMultiAlternatives(
        'LogIn', html_content, '', [obj.email], )
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
