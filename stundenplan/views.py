from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from stundenplan import get_plan
from django.shortcuts import render
from .get_plan import get_plan

@login_required
def index_view(request, klassenname):
    #usernamw
    user = request.user

    if request.user.is_superuser or request.user.profile.klasse.name == klassenname:
        context = get_plan(user, klassenname)
        return render(request, 'index.html', context)
    else:
        return render(request, '404.html')

def default_view(request):
    return render(request, 'default.html')