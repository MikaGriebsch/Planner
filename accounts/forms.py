from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label="E-mail Addresse",
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'E-Mail',
            'autocomplete': 'email',  # Browser erkennt dies als E-Mail-Feld
            'maxlength': '100'  # Maximale Länge der E-Mail-Adresse
        }),
        help_text="Your email address must be valid and unique."
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Username',
            'autocomplete': 'username',  # Username wird automatisch erkannt
            'maxlength': '100'  # Maximale Länge des Benutzernamens
        }),
        help_text="Your username must be unique and contain only letters, numbers and underscores."
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password',
            'autocomplete': 'new-password',  # Neues Passwort wird erkannt
            'minlength': '8',  # Minimale Länge des Passworts
            'maxlength': '100'  # Maximale Länge des Passworts
        }),
        help_text="Your password must be at least 8 characters long and contain letters and numbers."
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm Password',
            'autocomplete': 'new-password',  # Bestätigung des neuen Passworts
            'minlength': '8',  # Minimale Länge des Passworts
            'maxlength': '100'  # Maximale Länge des Passworts
        }),
        help_text="Enter the same password as above, for verification."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
