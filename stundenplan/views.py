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
    teacher_queryset = Teacher.objects.all()
    subject_queryset = Subject.objects.all()
    room_queryset = Room.objects.all()

    teacher_form_set = TeacherFormSet(prefix="teacher", queryset=teacher_queryset)
    subject_form_set = SubjectFormSet(prefix="subject", queryset=subject_queryset)  
    room_form_set = RoomFormSet(prefix="room", queryset=room_queryset)

    return render(request, 'input.html', {
        'teacher_form_set': teacher_form_set,
        'subject_form_set': subject_form_set,
        'room_form_set': room_form_set
        })

@require_POST
def save_input(request):
    valid = True

    print("Posted ID fields:")
    for key in request.POST.keys():
        if '-id' in key:
            print(f"{key}: {request.POST[key]}")

    teacher_queryset = Teacher.objects.all()
    subject_queryset = Subject.objects.all()
    room_queryset = Room.objects.all()

    teacher_form_set = TeacherFormSet(request.POST, prefix="teacher", queryset=teacher_queryset)
    subject_form_set = SubjectFormSet(request.POST, prefix="subject", queryset=subject_queryset)
    room_form_set = RoomFormSet(request.POST, prefix="room", queryset=room_queryset)
    
    if teacher_form_set.is_valid():
        teacher_form_set.save()
        print("Saved teachers successfully")
    else:
        valid = False

    if subject_form_set.is_valid():
        subject_form_set.save()
        print("Saved subjects successfully")
    else:
        valid = False
    
    if room_form_set.is_valid():
        room_form_set.save()
        print("Saved rooms successfully")
    else:
        valid = False

    if valid:
        return redirect("/schedule/create")
    else:
        # Fehlerausgabe
        if not teacher_form_set.is_valid():
            print(f"Unable to save teachers: {teacher_form_set.errors}")
        
        if not subject_form_set.is_valid():
            print(f"Unable to save subjects: {subject_form_set.errors}")
        
        if not room_form_set.is_valid():
            print(f"Unable to save rooms: {room_form_set.errors}")
        
        return render(request, 'input.html', {
            'teacher_form_set': teacher_form_set,
            'subject_form_set': subject_form_set,
            'room_form_set': room_form_set,
        })

