
from django.contrib.auth.views import LoginView
from django.urls import reverse
from stundenplan.models import Subject, Class
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def index_view(request, klassenname):
    monA1 = "IF"
    monA1Name = "Wf"
    monA1Nr = "1.5"

    subjects = Subject.objects.all()
    
    if Class.objects.filter(name=klassenname).exists():
        return render(request, 'index.html', {
            # Klassenname
            'klassenname': klassenname,

            # Erste Stunde
            'subjects': subjects, 
            'monA1': monA1, 
            'monA1Name': monA1Name, 
            'monA1Nr': monA1Nr
        })
    else:
        return render(request, 'class_not_found.html', {'klassenname': klassenname})

def default_view(request):
    return render(request, 'default.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


class CustomLoginView(LoginView):
    def get_success_url(self):
        if hasattr(self.request.user, 'profile') and self.request.user.profile.grade_with_char:
            klassenname = self.request.user.profile.grade_with_char.name
            return reverse('index_view', kwargs={'klassenname': klassenname})
        
        return '/default/'
