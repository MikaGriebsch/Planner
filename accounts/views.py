from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

# Create your views here.
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
            bezeichnung = self.request.user.profile.klasse.bezeichnung
            return reverse('index_view', kwargs={'bezeichnung': bezeichnung})
        
        return '/schedule/default/'