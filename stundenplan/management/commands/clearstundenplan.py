from django.core.management.base import BaseCommand
from stundenplan.models import Lesson

class Command(BaseCommand):
    help = 'Löscht alle Stundenplan-Einträge (Lessons) aus der Datenbank'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Löscht alle Einträge ohne Bestätigung',
        )

    def handle(self, *args, **options):
        if not options['force']:
            confirm = input('Sind Sie sicher, dass Sie ALLE Lesson-Einträge löschen möchten? (yes/no): ')
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.WARNING('Löschvorgang abgebrochen.'))
                return

        deleted_count, _ = Lesson.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Erfolgreich {deleted_count} Lesson-Einträge gelöscht.'))