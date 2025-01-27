from .models import *

def custom_subject_filter(klasse, lesson_number, weekday):
    return Lesson.objects.filter(
        klasse = klasse,
        lesson_number="1",
        weekday="MO"
    ).first().subject.abkuerzung

def custom_teacher_filter(klasse, lesson_number, weekday):
    return Lesson.objects.filter(
        klasse = klasse,
        lesson_number="1",
        weekday="MO"
    ).first().teacher.short_name

def get_plan(user, klassenname):
    klasse = user.profile.klasse
    monA1 = custom_subject_filter(klasse, "1", "MO")
    monA1Name = custom_teacher_filter(klasse, "1", "MO")
    monA1Nr = "1.5"

    return {
        'username': user.username,
        'klassenname': klassenname,
        'monA1': monA1,
        'monA1Name': monA1Name,
        'monA1Nr': monA1Nr,
    }
