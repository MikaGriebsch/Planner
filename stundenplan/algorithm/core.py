from stundenplan.models import Class
from .generator import StundenplanGenerator


class StundenplanCore:
    def __init__(self):
        self.generator = StundenplanGenerator()

    def generate_full_schedule(self):
        self.generator.cleanup()
        total_errors = 1000
        while total_errors > 0:
            for klasse in Class.objects.all():
                total_errors = self.generator.generate(klasse)

            if total_errors == 0:
                print("Stundenplan erfolgreich generiert!")
                return True
            else:
                print(f"Generierung abgeschlossen mit {total_errors} Fehlern")
                return False