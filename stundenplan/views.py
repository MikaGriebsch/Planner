import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from stundenplan import get_plan
from django.shortcuts import render
from stundenplan.models import Teacher
from .get_plan import get_plan
from .forms import *
from django.http import JsonResponse
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.core.exceptions import ValidationError
from stundenplan.models import Subject


@login_required
def index_view(request, bezeichnung):
    
    user = request.user

    if request.user.is_superuser or request.user.profile.klasse.bezeichnung == bezeichnung:
        context = get_plan(user, bezeichnung)
        return render(request, 'index.html', context)

def default_view(request):
    return render(request, 'default.html')

@login_required
def input_view(request):
    if not request.user.is_superuser:
        return render('404.html')

    teacher_form_set = TeacherFormSet(prefix="teacher", queryset=Teacher.objects.all())
    subject_form_set = SubjectFormSet(prefix="subject", queryset=Subject.objects.all())  
    room_form_set = RoomFormSet(prefix="room", queryset=Room.objects.all())
    grade_form_set = GradeFormSet(prefix="grade", queryset=Grade.objects.all().order_by('name'))

    # Initiierung Class Formsets
    class_form_sets = {
        grade.pk: ClassFormSet(
            instance=grade, 
            prefix=f"class{grade.pk}",
            queryset=Class.objects.filter(grade=grade)
        ) for grade in Grade.objects.all().order_by('name')
    }
    some_class_formset = ClassFormSet()
    empty_class_form = some_class_formset.empty_form if some_class_formset else None

    # Initiierung SubjectGrade Formsets
    subject_grade_form_sets = {
        grade.pk: SubjectGradeFormSet(
            instance=grade, 
            prefix=f"subject_grade{grade.pk}",
            queryset=Subject_Grade.objects.filter(grade=grade)
        ) for grade in Grade.objects.all()
    }
    some_subject_grade_formset = SubjectGradeFormSet()
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
        if '-DELETE' in key:
            print(f"{key}: {request.POST[key]}")

    teacher_form_set = TeacherFormSet(request.POST, prefix="teacher", queryset=Teacher.objects.all())
    subject_form_set = SubjectFormSet(request.POST, prefix="subject", queryset=Subject.objects.all())
    room_form_set = RoomFormSet(request.POST, prefix="room", queryset=Room.objects.all())
    grade_form_set = GradeFormSet(request.POST, prefix="grade", queryset=Grade.objects.all())

    # Initiierung Class Formsets
    class_form_sets = {
        grade.pk: ClassFormSet(
            request.POST,
            instance=grade, 
            prefix=f"class{grade.pk}",
        ) for grade in Grade.objects.all()
    }

    # Initiierung SubjectGrade Formsets
    subject_grade_form_sets = {
        grade.pk: SubjectGradeFormSet(
            request.POST,
            instance=grade, 
            prefix=f"subject_grade{grade.pk}",
        ) for grade in Grade.objects.all()
    }

    # eigentliche Subject Validierung mit AJAX (save_subject)
    if not subject_form_set.is_valid():
        for subject in subject_form_set:
            instance = subject.instance
            print(instance)
            if Subject.objects.filter(name=instance.name, abkuerzung=instance.abkuerzung).exists():
                continue
            elif not instance.id:
                continue    
            else:
                valid = False
                print(f"Subject {subject.instance.pk} is invalid: {subject.errors}")
    
    # Teacher Validierung
    if teacher_form_set.is_valid():
        teacher_form_set.save()
        print("Saved teachers successfully")
    else:
        valid = False
        print(f"Unable to save teachers: {teacher_form_set.errors}")
        form_errors = True
    
    # Room Validierung
    if room_form_set.is_valid():
        room_form_set.save()
        print("Saved rooms successfully")
    else:
        valid = False
        print(f"Unable to save rooms: {room_form_set.errors}")
    
    # eigentliche Grade Validierung mit AJAX
    if not grade_form_set.is_valid():
        for grade in grade_form_set:
            instance = grade.instance
            print(instance)
            if Grade.objects.filter(name=instance.name).exists():
                continue
            else:
                valid = False
                print(f"Grade {instance.pk} is invalid: {grade.errors}")

    # Validierung Class und Subject_Grade
    for grade in Grade.objects.all():
        has_subject_grade_data = False
        has_class_data = False
        
        for key in request.POST.keys():
            if f"subject_grade{grade.pk}-" in key and not key.endswith('TOTAL_FORMS'):
                has_subject_grade_data = True
            if f"class{grade.pk}-" in key and not key.endswith('TOTAL_FORMS'):
                has_class_data = True
        
        if not has_subject_grade_data and not has_class_data:
            print(f"No additional data for Grade {grade.name}. This is likely a new grade.")
            continue
        
        # Validierung Subject_Grade
        if has_subject_grade_data:
            subject_grade_form_set = subject_grade_form_sets[grade.pk]
            if subject_grade_form_set.is_valid():
                subject_grade_form_set.save()
                print(f"Saved subjects for grade {grade.name} successfully")
            else:
                valid = False
                print(f"Unable to save subjects for Grade {grade.name}: {subject_grade_form_set.errors}")
        
        # Validierung Class
        if has_class_data:
            class_form_set = class_form_sets[grade.pk]
            if class_form_set.is_valid():
                class_form_set.save()
                print(f"Saved classes for grade {grade.name} successfully")
            else:
                valid = False
                print(f"Unable to save classes for Grade {grade.name}: {class_form_set.errors}")


    if valid:
        return redirect("/admin")
    else:
        # empty forms für Erstellung neuer Forms
        some_class_formset = next(iter(class_form_sets.values()), ClassFormSet())
        empty_class_form = some_class_formset.empty_form if some_class_formset else None

        some_subject_grade_formset = next(iter(subject_grade_form_sets.values()), SubjectGradeFormSet())
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
            'form_errors': True,
        })

@require_POST
def save_subject(request):
    data = json.loads(request.body)
    payload = data.get('payload', {})

    subject_id = payload.get('id', '')

    # Delete
    if payload.get('delete'):
        try:
            subject = Subject.objects.get(pk=subject_id)
            has_references = False
            error_message = ""
            
            if Subject_Grade.objects.filter(subject=subject).exists():
                has_references = True
                error_message = "Fach kann nicht gelöscht werden, weil es von Klassenstufen verwendet wird."
            if Teacher.objects.filter(subjects=subject).exists():
                has_references = True
                error_message = "Fach kann nicht gelöscht werden, weil es von Lehrern unterrichtet wird."
            
            if has_references:
                return JsonResponse({
                    'success': False,
                    'message': error_message
                })
            subject_name = subject.name
            subject.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Fach "{subject_name}" wurde erfolgreich gelöscht.'
            })
            
        except Subject.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Fach nicht gefunden'
            })

    name = payload.get('name', '')
    abkuerzung = payload.get('abkuerzung', '')
    
    print(f"Received subject data: {payload}")
    
    if not name or not abkuerzung:
        return JsonResponse({
            'success': False,
            'message': 'Name und Abkürzung sind erforderlich'
        }, status=400)
    
    if subject_id:
        # Update
        try:
            subject = Subject.objects.get(pk=int(subject_id))
            subject.name = name
            subject.abkuerzung = abkuerzung
            subject.full_clean()
            subject.save()
            
            return JsonResponse({
                'success': True,
                'subject_id': subject.pk,
                'message': f'Fach {subject.name} aktualisiert'
            })
        except Subject.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Fach nicht gefunden'
            }, status=404)
        except ValidationError as e:
            return JsonResponse({
                'success': False,
                'message': str(e),
                'errors': dict(e) if hasattr(e, 'error_dict') else {'__all__': str(e)}
            }, status=400)
    else:
        # Neue Erstellung
        try:
            subject = Subject(name=name, abkuerzung=abkuerzung)
            subject.full_clean()  # Validiere vor dem Speichern
            subject.save()
            
            return JsonResponse({
                'success': True,
                'subject_id': subject.pk,
                'message': f'Neues Fach {subject.name} erstellt'
            })
        except ValidationError as e:
            return JsonResponse({
                'success': False,
                'message': str(e),
                'errors': dict(e) if hasattr(e, 'error_dict') else {'__all__': str(e)}
            }, status=400)

@require_GET
def get_subjects(request):
    try:
        subjects = Subject.objects.all()
        subjects_data = [
            {
                'id': subject.pk, 
                'name': subject.name, 
                'abkuerzung': subject.abkuerzung
            } for subject in subjects
        ]
        
        return JsonResponse({
            'success': True,
            'subjects': subjects_data
        })
    except Exception as e:
        import traceback
        print(f"Error in get_subjects: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({
            'success': False,
            'message': f'Fehler beim Abrufen der Fächer: {str(e)}'
        }, status=500)
    

@require_POST
def save_grade(request):
    data = json.loads(request.body)
    payload = data.get('payload', {})

    grade_id = payload.get('id', '')

    # Delete-Fall
    if payload.get('delete'):
        try:
            grade = Grade.objects.get(pk=grade_id)
            has_references = False
            error_message = ""
                
            grade_name = grade.name
            grade.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Klassenstufe "{grade_name}" wurde erfolgreich gelöscht.'
            })
            
        except Grade.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Klassenstufe nicht gefunden'
            })

    name = payload.get('name', '')
    
    print(f"Received grade data: {payload}")
    
    if not name:
        return JsonResponse({
            'success': False,
            'message': 'Name ist erforderlich'
        }, status=400)
    
    if grade_id:
        # Update
        try:
            grade = Grade.objects.get(pk=int(grade_id))
            # Check if another grade with the same name exists (excluding current one)
            if Grade.objects.filter(name=name).exclude(pk=int(grade_id)).exists():
                return JsonResponse({
                    'success': False,
                    'message': f'Eine Klassenstufe mit dem Namen "{name}" existiert bereits.'
                })
            grade.name = name
            grade.full_clean()
            grade.save()
            
            return JsonResponse({
                'success': True,
                'grade_id': grade.pk,
                'message': f'Klassenstufe {grade.name} aktualisiert'
            })
        except Grade.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Klassenstufe nicht gefunden'
            }, status=404)
        except ValidationError as e:
            return JsonResponse({
                'success': False,
                'message': str(e),
                'errors': dict(e) if hasattr(e, 'error_dict') else {'__all__': str(e)}
            }, status=400)
    else:
        # Neue Erstellung
        try:
            grade = Grade(name=name)
            grade.full_clean()  # Validiere vor dem Speichern
            grade.save()
            
            return JsonResponse({
                'success': True,
                'grade_id': grade.pk,
                'message': f'Neue Klassenstufe {grade.name} erstellt'
            })
        except ValidationError as e:
            return JsonResponse({
                'success': False,
                'message': str(e),
                'errors': dict(e) if hasattr(e, 'error_dict') else {'__all__': str(e)}
            }, status=400)

@require_GET
def get_grades(request):
    try:
        grades = Grade.objects.all().order_by('name')  # Sortierung nach Namen
        grades_data = [
            {
                'id': grade.pk, 
                'name': grade.name
            } for grade in grades
        ]
        
        return JsonResponse({
            'success': True,
            'grades': grades_data
        })
    except Exception as e:
        import traceback
        print(f"Error in get_grades: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({
            'success': False,
            'message': f'Fehler beim Abrufen der Klassenstufen: {str(e)}'
        }, status=500)
