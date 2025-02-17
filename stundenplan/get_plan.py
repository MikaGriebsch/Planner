from django.utils.functional import empty

from .models import *
from .models import Week


def custom_subject_filter(klasse, lesson_number, weekday, week_choice):
    week_instance = Week.objects.get(week_choice=week_choice)
    lesson = Lesson.objects.filter(
        klasse=klasse,
        lesson_number=lesson_number,
        weekday=weekday,
        week_choice=week_instance,
    ).first()
    return lesson.subject.abkuerzung if lesson else ""

def custom_teacher_filter(klasse, lesson_number, weekday, week_choice):
    week_instance = Week.objects.get(week_choice=week_choice)
    lesson = Lesson.objects.filter(
        klasse=klasse,
        lesson_number=lesson_number,
        weekday=weekday,
        week_choice=week_instance,
    ).first()
    return lesson.teacher.short_name if lesson else ""

def custom_room_filter(klasse, lesson_number, weekday, week_choice):
    week_instance = Week.objects.get(week_choice=week_choice)
    lesson = Lesson.objects.filter(
        klasse=klasse,
        lesson_number=lesson_number,
        weekday=weekday,
        week_choice=week_instance,
    ).first()
    return lesson.room_number if lesson else ""


def set_username(user):
    if user.first_name and user.last_name:
        username = user.first_name + " " + user.last_name
    else:
        username = user.username
    return username


def get_plan(user, bezeichnung):
    klasse = Class.objects.get(bezeichnung=bezeichnung)

    # Montag
    monA1 = custom_subject_filter(klasse, "1", "MO", "A")
    monA1Name = custom_teacher_filter(klasse, "1", "MO", "A")
    monA1Nr = custom_room_filter(klasse, "1", "MO", "A")
    monB1 = custom_subject_filter(klasse, "1", "MO", "B")
    monB1Name = custom_teacher_filter(klasse, "1", "MO", "B")
    monB1Nr = custom_room_filter(klasse, "1", "MO", "B")

    monA2 = custom_subject_filter(klasse, "2", "MO", "A")
    monA2Name = custom_teacher_filter(klasse, "2", "MO", "A")
    monA2Nr = custom_room_filter(klasse, "2", "MO", "A")
    monB2 = custom_subject_filter(klasse, "2", "MO", "B")
    monB2Name = custom_teacher_filter(klasse, "2", "MO", "B")
    monB2Nr = custom_room_filter(klasse, "2", "MO", "B")

    monA3_4 = custom_subject_filter(klasse, "3/4", "MO", "A")
    monA3_4Name = custom_teacher_filter(klasse, "3/4", "MO", "A")
    monA3_4Nr = custom_room_filter(klasse, "3/4", "MO", "A")
    monB3_4 = custom_subject_filter(klasse, "3/4", "MO", "B")
    monB3_4Name = custom_teacher_filter(klasse, "3/4", "MO", "B")
    monB3_4Nr = custom_room_filter(klasse, "3/4", "MO", "B")

    monA5_6 = custom_subject_filter(klasse, "5/6", "MO", "A")
    monA5_6Name = custom_teacher_filter(klasse, "5/6", "MO", "A")
    monA5_6Nr = custom_room_filter(klasse, "5/6", "MO", "A")
    monB5_6 = custom_subject_filter(klasse, "5/6", "MO", "B")
    monB5_6Name = custom_teacher_filter(klasse, "5/6", "MO", "B")
    monB5_6Nr = custom_room_filter(klasse, "5/6", "MO", "B")

    monA7_8 = custom_subject_filter(klasse, "7/8", "MO", "A")
    monA7_8Name = custom_teacher_filter(klasse, "7/8", "MO", "A")
    monA7_8Nr = custom_room_filter(klasse, "7/8", "MO", "A")
    monB7_8 = custom_subject_filter(klasse, "7/8", "MO", "B")
    monB7_8Name = custom_teacher_filter(klasse, "7/8", "MO", "B")
    monB7_8Nr = custom_room_filter(klasse, "7/8", "MO", "B")

    # Dienstag
    tueA1 = custom_subject_filter(klasse, "1", "DI", "A")
    tueA1Name = custom_teacher_filter(klasse, "1", "DI", "A")
    tueA1Nr = custom_room_filter(klasse, "1", "DI", "A")
    tueB1 = custom_subject_filter(klasse, "1", "DI", "B")
    tueB1Name = custom_teacher_filter(klasse, "1", "DI", "B")
    tueB1Nr = custom_room_filter(klasse, "1", "DI", "B")

    tueA2 = custom_subject_filter(klasse, "2", "DI", "A")
    tueA2Name = custom_teacher_filter(klasse, "2", "DI", "A")
    tueA2Nr = custom_room_filter(klasse, "2", "DI", "A")
    tueB2 = custom_subject_filter(klasse, "2", "DI", "B")
    tueB2Name = custom_teacher_filter(klasse, "2", "DI", "B")
    tueB2Nr = custom_room_filter(klasse, "2", "DI", "B")

    tueA3_4 = custom_subject_filter(klasse, "3/4", "DI", "A")
    tueA3_4Name = custom_teacher_filter(klasse, "3/4", "DI", "A")
    tueA3_4Nr = custom_room_filter(klasse, "3/4", "DI", "A")
    tueB3_4 = custom_subject_filter(klasse, "3/4", "DI", "B")
    tueB3_4Name = custom_teacher_filter(klasse, "3/4", "DI", "B")
    tueB3_4Nr = custom_room_filter(klasse, "3/4", "DI", "B")

    tueA5_6 = custom_subject_filter(klasse, "5/6", "DI", "A")
    tueA5_6Name = custom_teacher_filter(klasse, "5/6", "DI", "A")
    tueA5_6Nr = custom_room_filter(klasse, "5/6", "DI", "A")
    tueB5_6 = custom_subject_filter(klasse, "5/6", "DI", "B")
    tueB5_6Name = custom_teacher_filter(klasse, "5/6", "DI", "B")
    tueB5_6Nr = custom_room_filter(klasse, "5/6", "DI", "B")

    tueA7_8 = custom_subject_filter(klasse, "7/8", "DI", "A")
    tueA7_8Name = custom_teacher_filter(klasse, "7/8", "DI", "A")
    tueA7_8Nr = custom_room_filter(klasse, "7/8", "DI", "A")
    tueB7_8 = custom_subject_filter(klasse, "7/8", "DI", "B")
    tueB7_8Name = custom_teacher_filter(klasse, "7/8", "DI", "B")
    tueB7_8Nr = custom_room_filter(klasse, "7/8", "DI", "B")

    # Mittwoch
    wedA1 = custom_subject_filter(klasse, "1", "MI", "A")
    wedA1Name = custom_teacher_filter(klasse, "1", "MI", "A")
    wedA1Nr = custom_room_filter(klasse, "1", "MI", "A")
    wedB1 = custom_subject_filter(klasse, "1", "MI", "B")
    wedB1Name = custom_teacher_filter(klasse, "1", "MI", "B")
    wedB1Nr = custom_room_filter(klasse, "1", "MI", "B")

    wedA2 = custom_subject_filter(klasse, "2", "MI", "A")
    wedA2Name = custom_teacher_filter(klasse, "2", "MI", "A")
    wedA2Nr = custom_room_filter(klasse, "2", "MI", "A")
    wedB2 = custom_subject_filter(klasse, "2", "MI", "B")
    wedB2Name = custom_teacher_filter(klasse, "2", "MI", "B")
    wedB2Nr = custom_room_filter(klasse, "2", "MI", "B")

    wedA3_4 = custom_subject_filter(klasse, "3/4", "MI", "A")
    wedA3_4Name = custom_teacher_filter(klasse, "3/4", "MI", "A")
    wedA3_4Nr = custom_room_filter(klasse, "3/4", "MI", "A")
    wedB3_4 = custom_subject_filter(klasse, "3/4", "MI", "B")
    wedB3_4Name = custom_teacher_filter(klasse, "3/4", "MI", "B")
    wedB3_4Nr = custom_room_filter(klasse, "3/4", "MI", "B")

    wedA5_6 = custom_subject_filter(klasse, "5/6", "MI", "A")
    wedA5_6Name = custom_teacher_filter(klasse, "5/6", "MI", "A")
    wedA5_6Nr = custom_room_filter(klasse, "5/6", "MI", "A")
    wedB5_6 = custom_subject_filter(klasse, "5/6", "MI", "B")
    wedB5_6Name = custom_teacher_filter(klasse, "5/6", "MI", "B")
    wedB5_6Nr = custom_room_filter(klasse, "5/6", "MI", "B")

    wedA7_8 = custom_subject_filter(klasse, "7/8", "MI", "A")
    wedA7_8Name = custom_teacher_filter(klasse, "7/8", "MI", "A")
    wedA7_8Nr = custom_room_filter(klasse, "7/8", "MI", "A")
    wedB7_8 = custom_subject_filter(klasse, "7/8", "MI", "B")
    wedB7_8Name = custom_teacher_filter(klasse, "7/8", "MI", "B")
    wedB7_8Nr = custom_room_filter(klasse, "7/8", "MI", "B")

    # Donnerstag
    thuA1 = custom_subject_filter(klasse, "1", "DO", "A")
    thuA1Name = custom_teacher_filter(klasse, "1", "DO", "A")
    thuA1Nr = custom_room_filter(klasse, "1", "DO", "A")
    thuB1 = custom_subject_filter(klasse, "1", "DO", "B")
    thuB1Name = custom_teacher_filter(klasse, "1", "DO", "B")
    thuB1Nr = custom_room_filter(klasse, "1", "DO", "B")

    thuA2 = custom_subject_filter(klasse, "2", "DO", "A")
    thuA2Name = custom_teacher_filter(klasse, "2", "DO", "A")
    thuA2Nr = custom_room_filter(klasse, "2", "DO", "A")
    thuB2 = custom_subject_filter(klasse, "2", "DO", "B")
    thuB2Name = custom_teacher_filter(klasse, "2", "DO", "B")
    thuB2Nr = custom_room_filter(klasse, "2", "DO", "B")

    thuA3_4 = custom_subject_filter(klasse, "3/4", "DO", "A")
    thuA3_4Name = custom_teacher_filter(klasse, "3/4", "DO", "A")
    thuA3_4Nr = custom_room_filter(klasse, "3/4", "DO", "A")
    thuB3_4 = custom_subject_filter(klasse, "3/4", "DO", "B")
    thuB3_4Name = custom_teacher_filter(klasse, "3/4", "DO", "B")
    thuB3_4Nr = custom_room_filter(klasse, "3/4", "DO", "B")

    thuA5_6 = custom_subject_filter(klasse, "5/6", "DO", "A")
    thuA5_6Name = custom_teacher_filter(klasse, "5/6", "DO", "A")
    thuA5_6Nr = custom_room_filter(klasse, "5/6", "DO", "A")
    thuB5_6 = custom_subject_filter(klasse, "5/6", "DO", "B")
    thuB5_6Name = custom_teacher_filter(klasse, "5/6", "DO", "B")
    thuB5_6Nr = custom_room_filter(klasse, "5/6", "DO", "B")

    thuA7_8 = custom_subject_filter(klasse, "7/8", "DO", "A")
    thuA7_8Name = custom_teacher_filter(klasse, "7/8", "DO", "A")
    thuA7_8Nr = custom_room_filter(klasse, "7/8", "DO", "A")
    thuB7_8 = custom_subject_filter(klasse, "7/8", "DO", "B")
    thuB7_8Name = custom_teacher_filter(klasse, "7/8", "DO", "B")
    thuB7_8Nr = custom_room_filter(klasse, "7/8", "DO", "B")

    # Freitag
    friA1 = custom_subject_filter(klasse, "1", "FR", "A")
    friA1Name = custom_teacher_filter(klasse, "1", "FR", "A")
    friA1Nr = custom_room_filter(klasse, "1", "FR", "A")
    friB1 = custom_subject_filter(klasse, "1", "FR", "B")
    friB1Name = custom_teacher_filter(klasse, "1", "FR", "B")
    friB1Nr = custom_room_filter(klasse, "1", "FR", "B")

    friA2 = custom_subject_filter(klasse, "2", "FR", "A")
    friA2Name = custom_teacher_filter(klasse, "2", "FR", "A")
    friA2Nr = custom_room_filter(klasse, "2", "FR", "A")
    friB2 = custom_subject_filter(klasse, "2", "FR", "B")
    friB2Name = custom_teacher_filter(klasse, "2", "FR", "B")
    friB2Nr = custom_room_filter(klasse, "2", "FR", "B")

    friA3_4 = custom_subject_filter(klasse, "3/4", "FR", "A")
    friA3_4Name = custom_teacher_filter(klasse, "3/4", "FR", "A")
    friA3_4Nr = custom_room_filter(klasse, "3/4", "FR", "A")
    friB3_4 = custom_subject_filter(klasse, "3/4", "FR", "B")
    friB3_4Name = custom_teacher_filter(klasse, "3/4", "FR", "B")
    friB3_4Nr = custom_room_filter(klasse, "3/4", "FR", "B")

    friA5_6 = custom_subject_filter(klasse, "5/6", "FR", "A")
    friA5_6Name = custom_teacher_filter(klasse, "5/6", "FR", "A")
    friA5_6Nr = custom_room_filter(klasse, "5/6", "FR", "A")
    friB5_6 = custom_subject_filter(klasse, "5/6", "FR", "B")
    friB5_6Name = custom_teacher_filter(klasse, "5/6", "FR", "B")
    friB5_6Nr = custom_room_filter(klasse, "5/6", "FR", "B")

    friA7_8 = custom_subject_filter(klasse, "7/8", "FR", "A")
    friA7_8Name = custom_teacher_filter(klasse, "7/8", "FR", "A")
    friA7_8Nr = custom_room_filter(klasse, "7/8", "FR", "A")
    friB7_8 = custom_subject_filter(klasse, "7/8", "FR", "B")
    friB7_8Name = custom_teacher_filter(klasse, "7/8", "FR", "B")
    friB7_8Nr = custom_room_filter(klasse, "7/8", "FR", "B")

    username = set_username(user)

    # Rückgabe des Stundenplans
    return {
        'username':  username,
        'klassenname': bezeichnung,
        # Montag
        'monA1': monA1, 'monA1Name': monA1Name, 'monA1Nr': monA1Nr,
        'monB1': monB1, 'monB1Name': monB1Name, 'monB1Nr': monB1Nr,
        'monA2': monA2, 'monA2Name': monA2Name, 'monA2Nr': monA2Nr,
        'monB2': monB2, 'monB2Name': monB2Name, 'monB2Nr': monB2Nr,
        'monA3_4': monA3_4, 'monA3_4Name': monA3_4Name, 'monA3_4Nr': monA3_4Nr,
        'monB3_4': monB3_4, 'monB3_4Name': monB3_4Name, 'monB3_4Nr': monB3_4Nr,
        'monA5_6': monA5_6, 'monA5_6Name': monA5_6Name, 'monA5_6Nr': monA5_6Nr,
        'monB5_6': monB5_6, 'monB5_6Name': monB5_6Name, 'monB5_6Nr': monB5_6Nr,
        'monA7_8': monA7_8, 'monA7_8Name': monA7_8Name, 'monA7_8Nr': monA7_8Nr,
        'monB7_8': monB7_8, 'monB7_8Name': monB7_8Name, 'monB7_8Nr': monB7_8Nr,
        # Dienstag
        'tueA1': tueA1, 'tueA1Name': tueA1Name, 'tueA1Nr': tueA1Nr,
        'tueB1': tueB1, 'tueB1Name': tueB1Name, 'tueB1Nr': tueB1Nr,
        'tueA2': tueA2, 'tueA2Name': tueA2Name, 'tueA2Nr': tueA2Nr,
        'tueB2': tueB2, 'tueB2Name': tueB2Name, 'tueB2Nr': tueB2Nr,
        'tueA3_4': tueA3_4, 'tueA3_4Name': tueA3_4Name, 'tueA3_4Nr': tueA3_4Nr,
        'tueB3_4': tueB3_4, 'tueB3_4Name': tueB3_4Name, 'tueB3_4Nr': tueB3_4Nr,
        'tueA5_6': tueA5_6, 'tueA5_6Name': tueA5_6Name, 'tueA5_6Nr': tueA5_6Nr,
        'tueB5_6': tueB5_6, 'tueB5_6Name': tueB5_6Name, 'tueB5_6Nr': tueB5_6Nr,
        'tueA7_8': tueA7_8, 'tueA7_8Name': tueA7_8Name, 'tueA7_8Nr': tueA7_8Nr,
        'tueB7_8': tueB7_8, 'tueB7_8Name': tueB7_8Name, 'tueB7_8Nr': tueB7_8Nr,
        # Mittwoch
        'wedA1': wedA1, 'wedA1Name': wedA1Name, 'wedA1Nr': wedA1Nr,
        'wedB1': wedB1, 'wedB1Name': wedB1Name, 'wedB1Nr': wedB1Nr,
        'wedA2': wedA2, 'wedA2Name': wedA2Name, 'wedA2Nr': wedA2Nr,
        'wedB2': wedB2, 'wedB2Name': wedB2Name, 'wedB2Nr': wedB2Nr,
        'wedA3_4': wedA3_4, 'wedA3_4Name': wedA3_4Name, 'wedA3_4Nr': wedA3_4Nr,
        'wedB3_4': wedB3_4, 'wedB3_4Name': wedB3_4Name, 'wedB3_4Nr': wedB3_4Nr,
        'wedA5_6': wedA5_6, 'wedA5_6Name': wedA5_6Name, 'wedA5_6Nr': wedA5_6Nr,
        'wedB5_6': wedB5_6, 'wedB5_6Name': wedB5_6Name, 'wedB5_6Nr': wedB5_6Nr,
        'wedA7_8': wedA7_8, 'wedA7_8Name': wedA7_8Name, 'wedA7_8Nr': wedA7_8Nr,
        'wedB7_8': wedB7_8, 'wedB7_8Name': wedB7_8Name, 'wedB7_8Nr': wedB7_8Nr,
        # Donnerstag
        'thuA1': thuA1, 'thuA1Name': thuA1Name, 'thuA1Nr': thuA1Nr,
        'thuB1': thuB1, 'thuB1Name': thuB1Name, 'thuB1Nr': thuB1Nr,
        'thuA2': thuA2, 'thuA2Name': thuA2Name, 'thuA2Nr': thuA2Nr,
        'thuB2': thuB2, 'thuB2Name': thuB2Name, 'thuB2Nr': thuB2Nr,
        'thuA3_4': thuA3_4, 'thuA3_4Name': thuA3_4Name, 'thuA3_4Nr': thuA3_4Nr,
        'thuB3_4': thuB3_4, 'thuB3_4Name': thuB3_4Name, 'thuB3_4Nr': thuB3_4Nr,
        'thuA5_6': thuA5_6, 'thuA5_6Name': thuA5_6Name, 'thuA5_6Nr': thuA5_6Nr,
        'thuB5_6': thuB5_6, 'thuB5_6Name': thuB5_6Name, 'thuB5_6Nr': thuB5_6Nr,
        'thuA7_8': thuA7_8, 'thuA7_8Name': thuA7_8Name, 'thuA7_8Nr': thuA7_8Nr,
        'thuB7_8': thuB7_8, 'thuB7_8Name': thuB7_8Name, 'thuB7_8Nr': thuB7_8Nr,
        # Freitag
        'friA1': friA1, 'friA1Name': friA1Name, 'friA1Nr': friA1Nr,
        'friB1': friB1, 'friB1Name': friB1Name, 'friB1Nr': friB1Nr,
        'friA2': friA2, 'friA2Name': friA2Name, 'friA2Nr': friA2Nr,
        'friB2': friB2, 'friB2Name': friB2Name, 'friB2Nr': friB2Nr,
        'friA3_4': friA3_4, 'friA3_4Name': friA3_4Name, 'friA3_4Nr': friA3_4Nr,
        'friB3_4': friB3_4, 'friB3_4Name': friB3_4Name, 'friB3_4Nr': friB3_4Nr,
        'friA5_6': friA5_6, 'friA5_6Name': friA5_6Name, 'friA5_6Nr': friA5_6Nr,
        'friB5_6': friB5_6, 'friB5_6Name': friB5_6Name, 'friB5_6Nr': friB5_6Nr,
        'friA7_8': friA7_8, 'friA7_8Name': friA7_8Name, 'friA7_8Nr': friA7_8Nr,
        'friB7_8': friB7_8, 'friB7_8Name': friB7_8Name, 'friB7_8Nr': friB7_8Nr
    }
