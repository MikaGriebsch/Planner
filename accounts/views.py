from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import get_user_model


# Create your views here.
def first_login(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'first_login.html', {'form': form})

class CustomLoginView(LoginView):
    def get_success_url(self):
        first_login = self.request.session.pop('first_login', False)

        if first_login:
            return '/first_login/'
        
        if hasattr(self.request.user, 'profile') and self.request.user.profile.klasse:
            bezeichnung = self.request.user.profile.klasse.bezeichnung
            return reverse('index_view', kwargs={'bezeichnung': bezeichnung})
        
        return '/schedule/default/'