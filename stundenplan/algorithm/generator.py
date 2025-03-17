from django.db import transaction
from stundenplan.models import Lesson, Teacher, Subject, Class, Room, Week
import random


class StundenplanGenerator:
    def __init__(self):
        self.alle_lehrer = list(Teacher.objects.all())
        self.raeume = list(Room.objects.all())
        self.globaler_stundenplan = {day: {slot: [] for slot in ['1', '2', '3/4', '5/6', '7/8']} for day in
                                     ['MO', 'DI', 'MI', 'DO', 'FR']}
        self.fehlende_zuweisungen = 0
        self.week = Week.objects.first()

    def _freier_raum(self, tag, timeslot):
        belegte_raeume = set(
            lesson.room_number.room_number
            for lesson in Lesson.objects.filter(
                weekday=tag,
                lesson_number=timeslot,
                week_choice=self.week
            )
        )
        for raum in self.raeume:
            if raum.room_number not in belegte_raeume:
                return raum
        return None

    def _freier_lehrer(self, tag, timeslot, fach):
        kompetente_lehrer = Teacher.objects.filter(subjects=fach)
        gebundene_lehrer = set(
            lesson.teacher.id
            for lesson in Lesson.objects.filter(
                weekday=tag,
                lesson_number=timeslot,
                week_choice=self.week
            )
        )
        for lehrer in kompetente_lehrer:
            if lehrer.id not in gebundene_lehrer:
                return lehrer
        return None

    def _gueltige_stunde(self, tag, timeslot, kontingent, klasse):
        random.shuffle(kontingent)
        for stunde in kontingent:
            lehrer = self._freier_lehrer(tag, timeslot, stunde['fach'])
            raum = self._freier_raum(tag, timeslot)
            if lehrer and raum:
                kontingent.remove(stunde)
                return {
                    'lehrer': lehrer,
                    'fach': stunde['fach'],
                    'raum': raum,
                    'dauer': stunde['dauer']
                }
        return None

    @transaction.atomic
    def generate(self, klasse):
        subjects_grade = klasse.grade.subject_grade_set.all()
        bricks = []
        slabs = []

        for sg in subjects_grade:
            wochenstunden = sg.wochenstunden
            if wochenstunden % 2 == 1:
                slabs.append({'fach': sg.subject, 'dauer': 1})
                wochenstunden -= 1
            bricks.extend([{'fach': sg.subject, 'dauer': 2}] * (wochenstunden // 2))

        for day in ['MO', 'DI', 'MI', 'DO', 'FR']:
            for slot in ['1', '2']:
                if not slabs:
                    break
                stunde = self._gueltige_stunde(day, slot, slabs, klasse)
                if stunde:
                    Lesson.objects.create(
                        lesson_number=slot,
                        weekday=day,
                        teacher=stunde['lehrer'],
                        subject=stunde['fach'],
                        klasse=klasse,
                        room_number=stunde['raum'],
                        week_choice=self.week
                    )
                else:
                    print(f"Fehler: Keine gültige Stunde gefunden für {klasse} am {day} in Slot {slot} (Slab)")

        for day in ['MO', 'DI', 'MI', 'DO', 'FR']:
            for slot in ['3/4', '5/6']:
                if not bricks:
                    break
                stunde = self._gueltige_stunde(day, slot, bricks, klasse)
                if stunde:
                    Lesson.objects.create(
                        lesson_number=slot,
                        weekday=day,
                        teacher=stunde['lehrer'],
                        subject=stunde['fach'],
                        klasse=klasse,
                        room_number=stunde['raum'],
                        week_choice=self.week
                    )
                else:
                    print(f"Fehler: Keine gültige Stunde gefunden für {klasse} am {day} in Slot {slot} (Brick)")

        saved_day = random.choice(['MO', 'DI', 'MI', 'DO', 'FR'])
        while bricks:
            day = random.choice(['MO', 'DI', 'MI', 'DO', 'FR'])
            while saved_day == day:
                day = random.choice(['MO', 'DI', 'MI', 'DO', 'FR'])
            saved_day = day
            stunde = self._gueltige_stunde(day, '7/8', bricks, klasse)
            if stunde:
                Lesson.objects.create(
                    lesson_number='7/8',
                    weekday=day,
                    teacher=stunde['lehrer'],
                    subject=stunde['fach'],
                    klasse=klasse,
                    room_number=stunde['raum'],
                    week_choice=self.week
                )
            else:
                print(f"Fehler: Keine gültige Stunde gefunden für {klasse} am {day} in Slot 7/8 (Brick)")
                break

        remaining = len(slabs) + len(bricks)
        if remaining > 0:
            self.fehlende_zuweisungen += remaining
            print(f"Warnung: {remaining} Stunden konnten nicht zugeordnet werden für {klasse}")

        return self.fehlende_zuweisungen

    def cleanup(self):
        Lesson.objects.all().delete()