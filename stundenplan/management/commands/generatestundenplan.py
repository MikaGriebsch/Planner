from django.core.management.base import BaseCommand
from stundenplan.algorithm.core import StundenplanCore


class Command(BaseCommand):
    help = 'Generiert den Stundenplan'

    def handle(self, *args, **options):
        core = StundenplanCore()
        success = core.generate_full_schedule()
        if success:
            self.stdout.write(self.style.SUCCESS('Stundenplan generiert'))
        else:
            self.stdout.write(self.style.ERROR('Fehler bei der Generierung'))