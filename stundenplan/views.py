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

    teacher_form_set = TeacherFormSet(prefix="teacher", queryset=Teacher.objects.all())
    subject_form_set = SubjectFormSet(prefix="subject", queryset=Subject.objects.all())  
    room_form_set = RoomFormSet(prefix="room", queryset=Room.objects.all())
    grade_form_set = GradeFormSet(prefix="grade", queryset=Grade.objects.all())

    # Initiierung Class Formsets
    class_form_sets = {
        grade.pk: ClassFormSet(
            instance=grade, 
            prefix=f"class{grade.pk}",
            queryset=Class.objects.filter(grade=grade)
        ) for grade in Grade.objects.all()
    }
    some_class_formset = next(iter(class_form_sets.values()), None)
    empty_class_form = some_class_formset.empty_form if some_class_formset else None

    # Initiierung SubjectGrade Formsets
    subject_grade_form_sets = {
        grade.pk: SubjectGradeFormSet(
            instance=grade, 
            prefix=f"subject_grade{grade.pk}",
            queryset=Subject_Grade.objects.filter(grade=grade)
        ) for grade in Grade.objects.all()
    }
    some_subject_grade_formset = next(iter(subject_grade_form_sets.values()), None)
    empty_subject_grade_form = some_subject_grade_formset.empty_form if some_subject_grade_formset else None

    return render(request, 'input.html', {
        'teacher_form_set': teacher_form_set,
        'subject_form_set': subject_form_set,
        'room_form_set': room_form_set,
        'grade_form_set': grade_form_set,
        'class_form_sets': class_form_sets,
        'empty_class_form': empty_class_form,
        'subject_grade_form_sets': subject_grade_form_sets,
        'empty_subject_grade_form': empty_subject_grade_form,
        })

@require_POST
def save_input(request):
    valid = True

    print("Posted ID fields:")
    for key in request.POST.keys():
        if '-id' in key:
            print(f"{key}: {request.POST[key]}")

    teacher_form_set = TeacherFormSet(request.POST, prefix="teacher", queryset=Teacher.objects.all())
    subject_form_set = SubjectFormSet(request.POST, prefix="subject", queryset=Subject.objects.all())
    room_form_set = RoomFormSet(request.POST, prefix="room", queryset=Room.objects.all())
    grade_form_set = GradeFormSet(request.POST, prefix="grade", queryset=Grade.objects.all())
    
    # Teacher Validierung
    if teacher_form_set.is_valid():
        teacher_form_set.save()
        print("Saved teachers successfully")
    else:
        valid = False
        print(f"Unable to save teachers: {teacher_form_set.errors}")

    # Subject Validierung
    if subject_form_set.is_valid():
        subject_form_set.save()
        print("Saved subjects successfully")
    else:
        valid = False
        print(f"Unable to save subjects: {subject_form_set.errors}")
        

    # Room Validierung
    if room_form_set.is_valid():
        room_form_set.save()
        print("Saved rooms successfully")
    else:
        valid = False
        print(f"Unable to save rooms: {room_form_set.errors}")
    
    # Grade Validierung
    if grade_form_set.is_valid():
        grade_form_set.save()
        print("Saved grades successfully")

        all_grades = Grade.objects.all()

        for grade in all_grades:
            subject_grade_form_set = SubjectGradeFormSet(
                request.POST, 
                instance=grade,
                prefix=f"subject_grade{grade.pk}",
                queryset=Subject_Grade.objects.filter(grade=grade)
            )
            if subject_grade_form_set.is_valid():
                subject_grade_form_set.save()
                print(f"Saved subjects for grade {grade.name} successfully")
            else:
                valid = False
                print(f"Unable to save subjects for Grade {grade.name}: {subject_grade_form_set.errors}")

        # Class Validierung
        for grade in all_grades:
            class_form_set = ClassFormSet(
                request.POST, 
                instance=grade,
                prefix=f"class{grade.pk}",
                queryset=Class.objects.filter(grade=grade)
            )
            if class_form_set.is_valid():
                class_form_set.save()
                print(f"Saved classes for grade {grade.name} successfully")
            else:
                valid = False
                print(f"Unable to save classes for Grade {grade.name}: {class_form_set.errors}")
    else:
        valid = False
        print(f"Unable to save grades: {grade_form_set.errors}")


    if valid:
        return redirect("/schedule/create")
    else:
        # Initiierung Class Formsets
        class_form_sets = {
            grade.pk: ClassFormSet(
                instance=grade, 
                prefix=f"class{grade.pk}",
                queryset=Class.objects.filter(grade=grade)
            ) for grade in Grade.objects.all()
        }
        some_class_formset = next(iter(class_form_sets.values()), None)
        empty_class_form = some_class_formset.empty_form if some_class_formset else None

        # Initiierung SubjectGrade Formsets
        subject_grade_form_sets = {
            grade.pk: SubjectGradeFormSet(
                instance=grade, 
                prefix=f"subject_grade{grade.pk}",
                queryset=Subject_Grade.objects.filter(grade=grade)
            ) for grade in Grade.objects.all()
        }
        some_subject_grade_formset = next(iter(subject_grade_form_sets.values()), None)
        empty_subject_grade_form = some_subject_grade_formset.empty_form if some_subject_grade_formset else None

        return render(request, 'input.html', {
            'teacher_form_set': teacher_form_set,
            'subject_form_set': subject_form_set,
            'room_form_set': room_form_set,
            'grade_form_set': grade_form_set,
            'class_form_sets': class_form_sets,
            'empty_class_form': empty_class_form,
            'subject_grade_form_sets': subject_grade_form_sets,
            'empty_subject_grade_form': empty_subject_grade_form,
        })
    