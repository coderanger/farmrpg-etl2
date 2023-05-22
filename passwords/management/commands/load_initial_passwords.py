import json
from pathlib import Path

from django.core.management.base import BaseCommand

from passwords.models import Password, PasswordGroup


FIXTURES_ROOT = Path(__file__).joinpath("../../../fixtures").resolve()


class Command(BaseCommand):
    help = "Load initial passwords data"

    def handle(self, *args, **options):
        data = json.load(FIXTURES_ROOT.joinpath("initial_passwords.json").open("r"))
        for password in data:
            group, _ = PasswordGroup.objects.get_or_create(name=password["group"])
            Password.objects.filter(password=password["password"]).update(
                group=group,
                clue1=password["clue1"],
                clue2=password["clue2"],
                clue3=password["clue3"],
            )
