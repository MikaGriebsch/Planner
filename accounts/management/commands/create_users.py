import random
import string
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


def generate_password(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


class Command(BaseCommand):
    help = "Erstellt mehrere Benutzer mit fortlaufenden Nummern und speichert die Zugangsdaten in einer Datei."

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help="Anzahl der zu erstellenden Nutzer")

    def handle(self, *args, **options):
        num_users = options['count']
        last_user = User.objects.order_by('-username').first()
        last_number = int(last_user.username) if last_user and last_user.username.isdigit() else 0

        # Datei-Speicherort (anpassen, falls gewünscht)
        output_dir = os.path.join(os.path.dirname(__file__), "tmp")
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "user_credentials.txt")

        with open(output_file, "a") as file:  # "a" statt "w" → Datei wird erweitert
            for i in range(1, num_users + 1):
                username = f"{last_number + i:04d}"

                # Prüfen, ob der Benutzername bereits existiert
                while User.objects.filter(username=username).exists():
                    last_number += 1
                    username = f"{last_number + i:04d}"

                password = generate_password()
                User.objects.create_user(username=username, password=password)

                # Speichern der Anmeldedaten in der Datei
                file.write(f"Username: {username}, Password: {password}\n")

                self.stdout.write(self.style.SUCCESS(f"User {username} mit Passwort {password} erstellt."))

        self.stdout.write(self.style.SUCCESS(f"Alle Zugangsdaten wurden in {output_file} gespeichert."))
