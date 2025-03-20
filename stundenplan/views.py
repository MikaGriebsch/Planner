from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import redirect, render
from stundenplan import get_plan
from django.shortcuts import render

from stundenplan.models import Teacher
from .get_plan import get_plan
from django.http import HttpResponse
from django.views.decorators.http import require_POST
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
    teacher_form_set = TeacherFormSet(prefix="teacher")
    subject_form_set = SubjectFormSet(prefix="subject")

    return render(request, 'input.html', {
        'teacher_form_set': teacher_form_set,
        'subject_form_set': subject_form_set,
        })

@require_POST
def save_input(request):
    print(request.POST)
    print("")
    teacher_form_set = TeacherFormSet(request.POST, prefix="teacher")
    subject_form_set = SubjectFormSet(request.POST, prefix="subject")  

    teachers_valid = teacher_form_set.is_valid()
    subjects_valid = subject_form_set.is_valid()
    
    if teachers_valid and subjects_valid:
        teacher_form_set.save()
        subject_form_set.save()
        
        print("Saved teachers successfully")
        print("Saved subjects successfully")

        return redirect("/schedule/create") 
    else:
        # Fehlerausgabe
        if not teachers_valid:
            print(f"Unable to save teachers: {teacher_form_set.errors}")
        
        if not subjects_valid:
            print(f"Unable to save subjects: {subject_form_set.errors}")
        
        return render(request, 'input.html', {
            'teacher_form_set': teacher_form_set,
            'subject_form_set': subject_form_set,
        })

