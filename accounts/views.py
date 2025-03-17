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


        haeufigste_passwoerter = [
            "123456", "password", "123456789", "12345", "12345678",
            "qwerty", "123123", "111111", "abc123", "1234",
            "password1", "1234567", "1234567890", "123321", "000000",
            "iloveyou", "654321", "666666", "987654321", "123",
            "qwerty123", "1q2w3e4r", "sunshine", "admin", "welcome",
            "passw0rd", "letmein", "football", "monkey", "shadow",
            "696969", "superman", "hello", "trustno1", "killer",
            "zaq1zaq1", "dragon", "master", "qazwsx", "mustang",
            "jordan", "liverpool", "starwars", "cheese", "banana",
            "charlie", "michael", "ashley", "bailey", "football1"
        ]

        #print(request.POST)
        #print("Eingegebenes Passwort 1:", new_password1)
        #print("Eingegebenes Passwort 2:", new_password2)
        #print("Angemeldeter Benutzer:", request.user)
        if not new_password1 or not new_password2:
            messages.error(request, "Bitte geben Sie in jedes Feld das neue Passwort ein.")
        elif new_password1 != new_password2:
            messages.error(request, "Passwörter stimmen nicht überein.")
        elif len(new_password1) < 8:
            messages.error(request, "Passwort muss mindestens 8 Zeichen lang sein.")
        elif new_password1.isnumeric() or new_password1.isalpha():
            messages.error(request, "Passwort muss mindestens 1 Buchstaben und 1 Zahl enthalten.")
        elif new_password1 in haeufigste_passwoerter:
            messages.error(request, "Passwort ist zu unsicher.")
        else:
            user = request.user
            user.set_password(new_password1)
            user.save()
            # Profil anpassen
            if hasattr(user, 'profile'):
                user.profile.first_login = False
                user.profile.save()
                print(user.profile.first_login)
            update_session_auth_hash(request, user)
            klasse = getattr(user.profile, 'klasse', None) #gesichert zugriff auf Daten --> falls Klasse nicht vorhanden, wird None zurückgegeben
            bezeichnung = getattr(klasse, 'bezeichnung', None)

            if not bezeichnung:
                return redirect('/schedule/default/')
            return redirect('index_view', bezeichnung=bezeichnung)


       

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