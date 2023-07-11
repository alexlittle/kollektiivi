
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Import models from json"

    def add_arguments(self, parser):
        parser.add_argument(
            '-m',
            '--models',
            dest='models',
            help='Models to import',
        )

    def handle(self, *args, **options):

        models = options['models']
        if models == "all" or models == "tags":
            call_command('loaddata', "tags")

        if models == "all" or models == "pages":
            call_command('loaddata', "pages")

        if models == "all" or models == "news":
            call_command('loaddata', "news")

        if models == "all" or models == "members":
            call_command('loaddata', "members")
