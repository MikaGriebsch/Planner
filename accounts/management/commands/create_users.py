import csv
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
    help = "Erstellt mehrere Benutzer aus einer CSV-Datei mit Namen und speichert die Zugangsdaten."

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="Pfad zur CSV-Datei mit den Nutzerdaten")

    def handle(self, *args, **options):
        file_path = options['file_path']
        last_user = User.objects.order_by('-username').first()
        last_number = int(last_user.username) if last_user and last_user.username.isdigit() else 0

        output_file = os.path.join(os.path.dirname(file_path), "user_credentials.csv")
        write_header = not os.path.exists(output_file)

        encodings = ['utf-8', 'ISO-8859-1', 'Windows-1252']
        names = []

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    reader = csv.reader(file)
                    next(reader)
                    names = [row for row in reader if row]
                    break
            except UnicodeDecodeError:
                continue

        if not names:
            self.stdout.write(self.style.ERROR("Die Datei konnte mit keinem der unterstützten Zeichensätze gelesen werden."))
            return

        with open(output_file, "a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            if write_header:
                writer.writerow(["Benutzername", "Vorname", "Nachname", "Passwort"])

            for i, (first_name, last_name) in enumerate(names):
                username = f"{last_number + i + 1:04d}"

                while User.objects.filter(username=username).exists():
                    last_number += 1
                    username = f"{last_number + i + 1:04d}"

                password = generate_password()
                user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)

                writer.writerow([username, first_name, last_name, password])
                self.stdout.write(self.style.SUCCESS(f"User {username} ({first_name} {last_name}) mit Passwort {password} erstellt."))

        self.stdout.write(self.style.SUCCESS(f"Alle Zugangsdaten wurden in {output_file} gespeichert."))
