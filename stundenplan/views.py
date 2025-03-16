from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import render
from stundenplan import get_plan
from django.shortcuts import render

from stundenplan.models import Teacher
from .get_plan import get_plan
from django.http import HttpResponse
from .input_data.forms import *


@login_required
def index_view(request, bezeichnung):
    
    user = request.user

    if request.user.is_superuser or request.user.profile.klasse.bezeichnung == bezeichnung:
        context = get_plan(user, bezeichnung)
        return render(request, 'index.html', context)

def default_view(request):
    return render(request, 'default.html')

#@login_required
def input_view(request):
    if request.method == "POST":
        #Validierung der Lehrer
        teacher_form_set = TeacherFormSet(request.POST)
        if teacher_form_set.is_valid():
            teacher_form_set.save()
            print("saved")
        else:
            return 
    else: 
        teacher_form_set = TeacherFormSet()
    return render(request, 'input.html', {'teacher_form_set': teacher_form_set})
