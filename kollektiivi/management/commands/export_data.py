import os

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Export models to json"

    def add_arguments(self, parser):
        parser.add_argument(
            '-m',
            '--models',
            dest='models',
            help='Models to export',
        )
        
    def handle(self, *args, **options):

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        fixture_root = os.path.join(base_dir, 'fixtures')

        models = options['models']
        if models == "all" or models == "tags":
            tags_file = os.path.join(fixture_root, 'tags.json')
            with open(tags_file, 'w') as f:
                call_command('dumpdata', "kollektiivi.tag", indent=4, stdout=f)

        if models == "all" or models == "pages":
            pages_file = os.path.join(fixture_root, 'pages.json')
            with open(pages_file, 'w') as f:
                call_command('dumpdata', "kollektiivi.page", indent=4, stdout=f)

        if models == "all" or models == "members":
            members_file = os.path.join(fixture_root, 'members.json')
            with open(members_file, 'w') as f:
                call_command('dumpdata', "kollektiivi.member", indent=4, stdout=f)

        if models == "all" or models == "news":
            news_file = os.path.join(fixture_root, 'news.json')
            with open(news_file, 'w') as f:
                call_command('dumpdata', "blog.blog", indent=4, stdout=f)
