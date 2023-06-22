from django.core.management.base import BaseCommand
from django.utils.text import slugify

from kollektiivi.models import Page, Tag


class Command(BaseCommand):

    def handle(self, *args, **options):

        # page slugs
        pages = Page.objects.all()

        for p in pages:
            old_slug = p.slug
            new_slug = slugify(p.title_en)
            if old_slug != new_slug:
                p.slug = new_slug
                p.save()
                print("%s - %s" % (old_slug, new_slug))

        # tag slugs
        tags = Tag.objects.all()

        for t in tags:
            old_slug = t.slug
            new_slug = slugify(t.name_en)
            if old_slug != new_slug:
                t.slug = new_slug
                t.save()
                print("%s - %s" % (old_slug, new_slug))
