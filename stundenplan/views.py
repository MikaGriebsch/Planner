from django.contrib.auth.decorators import login_required
from stundenplan import get_plan
from .get_plan import get_plan
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

@login_required
def index_view(request, bezeichnung):
    
    user = request.user

    if request.user.is_superuser or request.user.profile.klasse.bezeichnung == bezeichnung:
        context = get_plan(user, bezeichnung)
        return render(request, 'index.html', context)
    else:
        return render(request, '404.html')

def default_view(request):
    return render(request, 'default.html')

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