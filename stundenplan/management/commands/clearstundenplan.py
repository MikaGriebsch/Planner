from django.core.management.base import BaseCommand
from stundenplan.models import Lesson

class Command(BaseCommand):
    help = 'Löscht alle Stundenplan-Einträge (Lessons) aus der Datenbank'

    def handle(self, *args, **options):
        deleted_count, _ = Lesson.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Erfolgreich {deleted_count} Lesson-Einträge gelöscht.'))