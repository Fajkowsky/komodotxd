from django.shortcuts import render

from forms import RegisterForm

def index(request):
    form = RegisterForm()
    return render(request, 'index.html', {'form': form})
