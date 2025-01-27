
from django.contrib.auth.views import LoginView
from django.urls import reverse
from stundenplan.models import Subject, Class
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import CustomUserCreationForm

from stundenplan import get_plan
from django.shortcuts import render
from .get_plan import get_plan

@login_required
def index_view(request, klassenname):
    #usernamw
    user = request.user

    if request.user.profile.klasse.name == klassenname:
        context = get_plan(user, klassenname)
        return render(request, 'index.html', context)
    else:
        return render(request, '404.html')

def default_view(request):
    return render(request, 'default.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

class CustomLoginView(LoginView):
    def get_success_url(self):
        if hasattr(self.request.user, 'profile') and self.request.user.profile.klasse:
            klassenname = self.request.user.profile.klasse.name
            return reverse('index_view', kwargs={'klassenname': klassenname})
        
        return '/default/'