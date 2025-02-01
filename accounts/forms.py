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
        }),
        help_text="Your email address must be valid and unique."
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Username'
        }),
        help_text="Your username must be unique and contain only letters, numbers and underscores."
    )


    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password'
        }),
        help_text="Your password must be at least 8 characters long and contain letters and numbers."

    )


    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm Password'
        }),
                help_text="Enter the same password as above, for verification."

    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
