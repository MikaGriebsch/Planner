from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required




# Create your views here.
@login_required
def first_login(request):
    if request.method == "POST":
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")


        #print(request.POST)
        #print("Eingegebenes Passwort 1:", new_password1)
        #print("Eingegebenes Passwort 2:", new_password2)
        #print("Angemeldeter Benutzer:", request.user)

        if new_password1 and new_password2 and new_password1 == new_password2:
            user = request.user
            user.set_password(new_password1)
            user.save()
            # Profil anpassen
            if hasattr(user, 'profile'):
                user.profile.first_login = False
                user.profile.save()
                print(user.profile.first_login)
            update_session_auth_hash(request, user)
            messages.success(request, "Dein Passwort wurde erfolgreich geändert!")
            bezeichnung = user.profile.klasse.bezeichnung
            return redirect('index_view', bezeichnung=bezeichnung)

        else:
            messages.error(request, "Passwörter stimmen nicht überein.")

    return render(request, "first_login.html", {"request": request})



class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user

        if hasattr(user, 'profile') and user.profile.first_login:
            return '/first_login/'
        
        if hasattr(user, 'profile') and user.profile.klasse:
            bezeichnung = self.request.user.profile.klasse.bezeichnung
            return reverse('index_view', kwargs={'bezeichnung': bezeichnung})
        
        return '/schedule/default/'
    
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('/')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })