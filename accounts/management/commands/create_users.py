import random
import string
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


def generate_password(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


class Command(BaseCommand):
    help = "Erstellt mehrere Benutzer mit fortlaufenden Nummern"

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help="Anzahl der zu erstellenden Nutzer")

    def handle(self, *args, **options):
        num_users = options['count']
        last_user = User.objects.order_by('-username').first()
        last_number = int(last_user.username) if last_user and last_user.username.isdigit() else 0

        for i in range(1, num_users + 1):
            username = f"{last_number + i:04d}"

            # Prüfen, ob der Benutzername bereits existiert
            while User.objects.filter(username=username).exists():
                last_number += 1
                username = f"{last_number + i:04d}"

            password = generate_password()
            User.objects.create_user(username=username, password=password)
            self.stdout.write(self.style.SUCCESS(f"User {username} mit Passwort {password} erstellt."))
