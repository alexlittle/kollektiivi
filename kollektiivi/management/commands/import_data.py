
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Import models from json"

    def handle(self, *args, **options):

        call_command('loaddata', "tags")

        call_command('loaddata', "pages")

        call_command('loaddata', "news")

        call_command('loaddata', "members")
