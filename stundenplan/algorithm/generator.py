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
        self.lehrer_zuordnung = {}  # Speichert die Lehrer-Fach-Zuordnung pro Klasse

    def _freier_raum(self, tag, timeslot, fach):
        belegte_raeume = set(
            lesson.room_number.room_number
            for lesson in Lesson.objects.filter(
                weekday=tag,
                lesson_number=timeslot,
                week_choice=self.week
            )
        )
        fachraeume = Room.objects.filter(faecher=fach)
        for raum in fachraeume:
            if raum.room_number not in belegte_raeume:
                return raum
        return None

    def _lehrer_frei(self, tag, timeslot, lehrer):
        if not lehrer:
            return False
        return not Lesson.objects.filter(
            weekday=tag,
            lesson_number=timeslot,
            teacher=lehrer,
            week_choice=self.week
        ).exists()

    def _get_random_lehrer(self, fach):
        kompetente_lehrer = Teacher.objects.filter(subjects=fach)
        if not kompetente_lehrer:
            return None
        return random.choice(kompetente_lehrer)

    def _gueltige_stunde(self, tag, timeslot, kontingent, klasse):
        if not kontingent:
            return None
            
        random.shuffle(kontingent)
        for stunde in kontingent:
            # Hole den bereits zugeordneten Lehrer für dieses Fach in dieser Klasse
            if klasse not in self.lehrer_zuordnung:
                self.lehrer_zuordnung[klasse] = {}
            
            if stunde['fach'] not in self.lehrer_zuordnung[klasse]:
                self.lehrer_zuordnung[klasse][stunde['fach']] = self._get_random_lehrer(stunde['fach'])
            
            lehrer = self.lehrer_zuordnung[klasse][stunde['fach']]
            
            if not lehrer:
                continue

            if not self._lehrer_frei(tag, timeslot, lehrer):
                continue

            raum = self._freier_raum(tag, timeslot, fach=stunde['fach'])
            if not raum:
                continue

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
        # Lösche bestehende Zuordnungen für diese Klasse
        Lesson.objects.filter(klasse=klasse, week_choice=self.week).delete()
        
        subjects_grade = klasse.grade.subject_grade_set.all()
        bricks = []
        slabs = []

        # Erstelle bricks und slabs
        for sg in subjects_grade:
            wochenstunden = sg.wochenstunden
            if wochenstunden % 2 == 1:
                slabs.append({'fach': sg.subject, 'dauer': 1})
                wochenstunden -= 1
            bricks.extend([{'fach': sg.subject, 'dauer': 2}] * (wochenstunden // 2))

        # Verteile Einzelstunden (slabs) - 1. und 2. Stunde für alle Tage
        for slot in ['1', '2']:
            for day in ['MO', 'DI', 'MI', 'DO', 'FR']:
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
            if not slabs:
                break

        # Verteile Doppelstunden (bricks) für 3/4 und 5/6 für alle Tage
        for slot in ['3/4', '5/6']:
            for day in ['MO', 'DI', 'MI', 'DO', 'FR']:
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
            if not bricks:
                break

        # Verteile übrige Doppelstunden für 7/8 für alle Tage
        slot = '7/8'
        days = ['MO', 'DI', 'MI', 'DO', 'FR']
        random.shuffle(days)
        for day in days:
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

        remaining = len(slabs) + len(bricks)
        if remaining > 0:
            self.fehlende_zuweisungen += remaining
            print(f"Warnung: {remaining} Stunden konnten nicht zugeordnet werden für {klasse}")

        return self.fehlende_zuweisungen

    def cleanup(self):
        Lesson.objects.all().delete()