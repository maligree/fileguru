from getpass import getpass

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = "Creates a regular (non-super) user."

    def add_arguments(self, parser):
        parser.add_argument("username", action="store", type=str)
        parser.add_argument("--email", action="store", type=str)
        parser.add_argument("--no-token", action="store_true")

    def handle(self, *args, **options):
        username = options["username"]
        email = options["email"] or f"{username}@example.com"

        password = getpass()
        if not password:
            raise CommandError("Password cannot be empty.")

        try:
            user = User.objects.create_user(
                username, f"{username}@example.com", password
            )
        except IntegrityError:
            raise CommandError("User already exists.")

        self.stdout.write(self.style.SUCCESS('Created "%s"' % username))

        if not options["no_token"]:
            token = Token.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS("API token created: %s" % token.key))
