from django.utils.functional import empty

from .models import *


def custom_subject_filter(klasse, lesson_number, weekday):
    lesson = Lesson.objects.filter(
        klasse=klasse,
        lesson_number=lesson_number,
        weekday=weekday
    ).first()
    return lesson.subject.abkuerzung if lesson else ""


def custom_teacher_filter(klasse, lesson_number, weekday):
    lesson = Lesson.objects.filter(
        klasse=klasse,
        lesson_number=lesson_number,
        weekday=weekday
    ).first()
    return lesson.teacher.short_name if lesson else ""


def custom_room_filter(klasse, lesson_number, weekday):
    lesson = Lesson.objects.filter(
        klasse=klasse,
        lesson_number=lesson_number,
        weekday=weekday
    ).first()
    return lesson.room_number if lesson else ""

def get_plan(user, klassenname):
    klasse = Class.objects.get(name=klassenname) # muss bei Erweiterung auf mehrere Schulen angepasst werden

    # Montag
    monA1 = custom_subject_filter(klasse, "1", "MO")
    monA1Name = custom_teacher_filter(klasse, "1", "MO")
    monA1Nr = custom_room_filter(klasse, "1", "MO")

    monA2 = custom_subject_filter(klasse, "2", "MO")
    monA2Name = custom_teacher_filter(klasse, "2", "MO")
    monA2Nr = custom_room_filter(klasse, "2", "MO")

    monA3_4 = custom_subject_filter(klasse, "3/4", "MO")
    monA3_4Name = custom_teacher_filter(klasse, "3/4", "MO")
    monA3_4Nr = custom_room_filter(klasse, "3/4", "MO")

    monA5_6 = custom_subject_filter(klasse, "5/6", "MO")
    monA5_6Name = custom_teacher_filter(klasse, "5/6", "MO")
    monA5_6Nr = custom_room_filter(klasse, "5/6", "MO")

    monA7_8 = custom_subject_filter(klasse, "7/8", "MO")
    monA7_8Name = custom_teacher_filter(klasse, "7/8", "MO")
    monA7_8Nr = custom_room_filter(klasse, "7/8", "MO")

    # Dienstag
    tueA1 = custom_subject_filter(klasse, "1", "DI")
    tueA1Name = custom_teacher_filter(klasse, "1", "DI")
    tueA1Nr = custom_room_filter(klasse, "1", "DI")

    tueA2 = custom_subject_filter(klasse, "2", "DI")
    tueA2Name = custom_teacher_filter(klasse, "2", "DI")
    tueA2Nr = custom_room_filter(klasse, "2", "DI")

    tueA3_4 = custom_subject_filter(klasse, "3/4", "DI")
    tueA3_4Name = custom_teacher_filter(klasse, "3/4", "DI")
    tueA3_4Nr = custom_room_filter(klasse, "3/4", "DI")

    tueA5_6 = custom_subject_filter(klasse, "5/6", "DI")
    tueA5_6Name = custom_teacher_filter(klasse, "5/6", "DI")
    tueA5_6Nr = custom_room_filter(klasse, "5/6", "DI")

    tueA7_8 = custom_subject_filter(klasse, "7/8", "DI")
    tueA7_8Name = custom_teacher_filter(klasse, "7/8", "DI")
    tueA7_8Nr = custom_room_filter(klasse, "7/8", "DI")

    # Mittwoch
    wedA1 = custom_subject_filter(klasse, "1", "MI")
    wedA1Name = custom_teacher_filter(klasse, "1", "MI")
    wedA1Nr = custom_room_filter(klasse, "1", "MI")

    wedA2 = custom_subject_filter(klasse, "2", "MI")
    wedA2Name = custom_teacher_filter(klasse, "2", "MI")
    wedA2Nr = custom_room_filter(klasse, "2", "MI")

    wedA3_4 = custom_subject_filter(klasse, "3/4", "MI")
    wedA3_4Name = custom_teacher_filter(klasse, "3/4", "MI")
    wedA3_4Nr = custom_room_filter(klasse, "3/4", "MI")

    wedA5_6 = custom_subject_filter(klasse, "5/6", "MI")
    wedA5_6Name = custom_teacher_filter(klasse, "5/6", "MI")
    wedA5_6Nr = custom_room_filter(klasse, "5/6", "MI")

    wedA7_8 = custom_subject_filter(klasse, "7/8", "MI")
    wedA7_8Name = custom_teacher_filter(klasse, "7/8", "MI")
    wedA7_8Nr = custom_room_filter(klasse, "7/8", "MI")

    # Donnerstag
    thuA1 = custom_subject_filter(klasse, "1", "DO")
    thuA1Name = custom_teacher_filter(klasse, "1", "DO")
    thuA1Nr = custom_room_filter(klasse, "1", "DO")

    thuA2 = custom_subject_filter(klasse, "2", "DO")
    thuA2Name = custom_teacher_filter(klasse, "2", "DO")
    thuA2Nr = custom_room_filter(klasse, "2", "DO")

    thuA3_4 = custom_subject_filter(klasse, "3/4", "DO")
    thuA3_4Name = custom_teacher_filter(klasse, "3/4", "DO")
    thuA3_4Nr = custom_room_filter(klasse, "3/4", "DO")

    thuA5_6 = custom_subject_filter(klasse, "5/6", "DO")
    thuA5_6Name = custom_teacher_filter(klasse, "5/6", "DO")
    thuA5_6Nr = custom_room_filter(klasse, "5/6", "DO")

    thuA7_8 = custom_subject_filter(klasse, "7/8", "DO")
    thuA7_8Name = custom_teacher_filter(klasse, "7/8", "DO")
    thuA7_8Nr = custom_room_filter(klasse, "7/8", "DO")

    # Freitag
    friA1 = custom_subject_filter(klasse, "1", "FR")
    friA1Name = custom_teacher_filter(klasse, "1", "FR")
    friA1Nr = custom_room_filter(klasse, "1", "FR")

    friA2 = custom_subject_filter(klasse, "2", "FR")
    friA2Name = custom_teacher_filter(klasse, "2", "FR")
    friA2Nr = custom_room_filter(klasse, "2", "FR")

    friA3_4 = custom_subject_filter(klasse, "3/4", "FR")
    friA3_4Name = custom_teacher_filter(klasse, "3/4", "FR")
    friA3_4Nr = custom_room_filter(klasse, "3/4", "FR")

    friA5_6 = custom_subject_filter(klasse, "5/6", "FR")
    friA5_6Name = custom_teacher_filter(klasse, "5/6", "FR")
    friA5_6Nr = custom_room_filter(klasse, "5/6", "FR")

    friA7_8 = custom_subject_filter(klasse, "7/8", "FR")
    friA7_8Name = custom_teacher_filter(klasse, "7/8", "FR")
    friA7_8Nr = custom_room_filter(klasse, "7/8", "FR")

    if user.first_name is not None and user.last_name is not None:
        username = user.first_name + " " + user.last_name
    else:
        username = user.username

    # Rückgabe des Stundenplans
    return {
        'username':  username,
        'klassenname': klassenname,
        # Montag
        'monA1': monA1, 'monA1Name': monA1Name, 'monA1Nr': monA1Nr,
        'monA2': monA2, 'monA2Name': monA2Name, 'monA2Nr': monA2Nr,
        'monA3_4': monA3_4, 'monA3_4Name': monA3_4Name, 'monA3_4Nr': monA3_4Nr,
        'monA5_6': monA5_6, 'monA5_6Name': monA5_6Name, 'monA5_6Nr': monA5_6Nr,
        'monA7_8': monA7_8, 'monA7_8Name': monA7_8Name, 'monA7_8Nr': monA7_8Nr,
        # Dienstag
        'tueA1': tueA1, 'tueA1Name': tueA1Name, 'tueA1Nr': tueA1Nr,
        'tueA2': tueA2, 'tueA2Name': tueA2Name, 'tueA2Nr': tueA2Nr,
        'tueA3_4': tueA3_4, 'tueA3_4Name': tueA3_4Name, 'tueA3_4Nr': tueA3_4Nr,
        'tueA5_6': tueA5_6, 'tueA5_6Name': tueA5_6Name, 'tueA5_6Nr': tueA5_6Nr,
        'tueA7_8': tueA7_8, 'tueA7_8Name': tueA7_8Name, 'tueA7_8Nr': tueA7_8Nr,
        # Mittwoch
        'wedA1': wedA1, 'wedA1Name': wedA1Name, 'wedA1Nr': wedA1Nr,
        'wedA2': wedA2, 'wedA2Name': wedA2Name, 'wedA2Nr': wedA2Nr,
        'wedA3_4': wedA3_4, 'wedA3_4Name': wedA3_4Name, 'wedA3_4Nr': wedA3_4Nr,
        'wedA5_6': wedA5_6, 'wedA5_6Name': wedA5_6Name, 'wedA5_6Nr': wedA5_6Nr,
        'wedA7_8': wedA7_8, 'wedA7_8Name': wedA7_8Name, 'wedA7_8Nr': wedA7_8Nr,
        # Donnerstag
        'thuA1': thuA1, 'thuA1Name': thuA1Name, 'thuA1Nr': thuA1Nr,
        'thuA2': thuA2, 'thuA2Name': thuA2Name, 'thuA2Nr': thuA2Nr,
        'thuA3_4': thuA3_4, 'thuA3_4Name': thuA3_4Name, 'thuA3_4Nr': thuA3_4Nr,
        'thuA5_6': thuA5_6, 'thuA5_6Name': thuA5_6Name, 'thuA5_6Nr': thuA5_6Nr,
        'thuA7_8': thuA7_8, 'thuA7_8Name': thuA7_8Name, 'thuA7_8Nr': thuA7_8Nr,
        # Freitag
        'friA1': friA1, 'friA1Name': friA1Name, 'friA1Nr': friA1Nr,
        'friA2': friA2, 'friA2Name': friA2Name, 'friA2Nr': friA2Nr,
        'friA3_4': friA3_4, 'friA3_4Name': friA3_4Name, 'friA3_4Nr': friA3_4Nr,
        'friA5_6': friA5_6, 'friA5_6Name': friA5_6Name, 'friA5_6Nr': friA5_6Nr,
        'friA7_8': friA7_8, 'friA7_8Name': friA7_8Name, 'friA7_8Nr': friA7_8Nr
    }
