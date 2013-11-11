from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core import mail
from django.template.loader import get_template
from django.template import Context

from forms import RegisterForm
from models import UserData

connection = mail.get_connection()


def index(request):
    data = {}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            obj, created = UserData.objects.get_or_create(
                username=cd['username'], email=cd['email'], is_active=False)
            if created:
                mail_activation(obj, cd)
                return HttpResponseRedirect('/thanks/')
            else:
                data['msg'] = 1
    else:
        data['form'] = RegisterForm()
    return render(request, 'index.html', data)


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


def thanks(request):
    return render(request, 'thanks.html')


def error(request):
    return render(request, '404.html')


def confirmation(request, userid):
    if UserData.objects.filter(confirmation=userid).update(is_active=True):
        return render(request, 'confirmation.html')
    else:
        return HttpResponseRedirect('/404/')
