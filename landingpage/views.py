from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.core import mail
from django.template.loader import get_template
from django.template import Context
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

from forms import RegisterForm, LoginForm, ModifyForm
from models import UserData

#make mail connection
connection = mail.get_connection()


def index(request, data={}):
    # function to handle two form on one page
    def handleforms(request, regform, logform):
        logging = loging(request, logform)
        registering = register(request, regform)
        if logging:
            return logging
        elif registering:
            return registering
        else:
            return False

    # validating register form
    def register(request, regform):
        if regform.is_valid():
            regcd = regform.cleaned_data
            obj, created = UserData.objects.get_or_create(
                username=regcd['username'], email=regcd['email'], is_active=False)

            if created:
                mail_activation(obj, regcd)

            return HttpResponseRedirect(reverse('thanks'))

    # validating login form
    def loging(request, logform):
        if logform.is_valid():
            logcd = logform.cleaned_data
            user = authenticate(
                userID=logcd['userID'], password=logcd['password'])

            if user is not None and user.is_active:
                login(request, user)

            return HttpResponseRedirect(reverse('account'))
    # --------------------------------------------------
    if request.method == 'POST':
        regform = RegisterForm(request.POST)
        logform = LoginForm(request.POST)
        forms_response = handleforms(request, regform, logform)
        if forms_response:
            return forms_response

    else:
        regform = RegisterForm()
        logform = LoginForm()

    return render(request, 'index.html', {'regform': regform, 'logform': logform, 'user': request.user})

# handle account request page
def account(request, data={}):
    if request.user.is_authenticated():
        data['user'] = request.user
        return render(request, 'account.html', data)
    else:
        return HttpResponseRedirect(reverse('error'))

# handle modify request page
def modify(request, data={}):
    if request.user.is_authenticated():
        logedUser = request.user
        if request.method == 'POST':
            form = ModifyForm(request.POST, request.FILES)
            if form.is_valid():
                user = UserData.objects.get(pk=logedUser.id)
                for attr, value in form.cleaned_data.iteritems():
                    if value:
                        setattr(user, attr, value)
                user.save()
                return HttpResponseRedirect(reverse('thanks'))
        else:
            user = model_to_dict(UserData.objects.get(pk=logedUser.id))
            form = ModifyForm(initial=user)
        return render(request, 'modify.html', {'form': form})
    else:
        return HttpResponseRedirect(reverse('error'))

# handle logout from session
def logouting(request):
    logout(request)
    return redirect('index')

# send activation mail with link
def mail_activation(obj, cd):
    connection.open()
    html_content = get_template('email/confirmation.html').render(
        Context({'code': obj.confirmation}))
    email = mail.EmailMultiAlternatives(
        'Activation link', html_content, '', [cd['email']], )
    email.attach_alternative(html_content, "text/html")
    connection.send_messages([email])
    connection.close()

# send mail with userID and password
def mail_login(obj, password):
    connection.open()
    html_content = get_template('email/login.html').render(
        Context({'login': obj.userID, 'password': password}))
    email = mail.EmailMultiAlternatives(
        'LogIn', html_content, '', [obj.email], )
    email.attach_alternative(html_content, "text/html")
    connection.send_messages([email])
    connection.close()

# handle tanks request page
def thanks(request):
    return render(request, 'thanks.html')

# handle error request page
def error(request):
    return render(request, '404.html')

# handle confirmation user request
def confirmation(request, userid):
    obj = get_object_or_404(UserData, confirmation=userid, is_active=False)
    mail_login(obj, obj.generate_auth())
    obj.save()
    return render(request, 'confirmation.html')
