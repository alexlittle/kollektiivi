from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.utils.text import slugify

from kollektiivi.models import Tracker


class Blog(models.Model):
    display_date = models.DateTimeField(default=timezone.now)
    title = models.TextField(blank=False)
    slug = models.SlugField()
    body = RichTextField()
    image = models.FileField(upload_to="images", blank=True, default=None)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name_fi)
        super(Blog, self).save(*args, **kwargs)

    def get_hits(self):
        return Tracker.objects.filter(url__endswith=self.slug).count()
