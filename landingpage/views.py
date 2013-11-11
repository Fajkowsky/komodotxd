from django.shortcuts import render
from django.http import HttpResponseRedirect

from forms import RegisterForm


def index(request):
    data = {}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponseRedirect('/thanks/')
    else:
        data['form'] = RegisterForm()
    return render(request, 'index.html', data)

def thanks(request):
    return render(request, 'thanks.html')