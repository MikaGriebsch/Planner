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
        parser.add_argument('count', type=int, help="Anzahl der zu erstellenden Nutzer")

    def handle(self, *args, **options):
        num_users = options['count']
        last_user = User.objects.order_by('-username').first()
        last_number = int(last_user.username) if last_user and last_user.username.isdigit() else 0

        input_dir = os.path.join(os.path.dirname(__file__), "tmp")
        os.makedirs(input_dir, exist_ok=True)
        csv_file = os.path.join(input_dir, "user_data.csv")


        output_file = os.path.join(input_dir, "user_credentials.csv")
        write_header = not os.path.exists(output_file)

        with open(csv_file, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            names = list(reader)

        if len(names) < num_users:
            self.stdout.write(self.style.ERROR("Nicht genügend Namen in der CSV-Datei!"))
            return

        with open(output_file, "a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            if write_header:
                writer.writerow(["Benutzername", "Vorname", "Nachname", "Passwort"])

            for i in range(num_users):
                first_name, last_name = names[i]
                username = f"{last_number + i + 1:04d}"

                while User.objects.filter(username=username).exists():
                    last_number += 1
                    username = f"{last_number + i + 1:04d}"

                password = generate_password()
                user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)

                writer.writerow([username, first_name, last_name, password])
                self.stdout.write(self.style.SUCCESS(f"User {username} ({first_name} {last_name}) mit Passwort {password} erstellt."))

        self.stdout.write(self.style.SUCCESS(f"Alle Zugangsdaten wurden in {output_file} gespeichert."))
