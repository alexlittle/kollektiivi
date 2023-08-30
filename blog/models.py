from django.conf import settings
from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from kollektiivi.models import Tracker


class Post(models.Model):
    display_date = models.DateTimeField(default=timezone.now)
    title = models.TextField(blank=False)
    slug = models.SlugField(blank=True, default=None, max_length=200)
    body = RichTextUploadingField()
    image = models.FileField(upload_to="images", blank=True, default=None)
    active = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   null=True,
                                   blank=True,
                                   default=None,
                                   on_delete=models.SET_NULL,
                                   related_name="post_created_by")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   null=True,
                                   blank=True,
                                   default=None,
                                   on_delete=models.SET_NULL,
                                   related_name="post_updated_by")
    class Meta:
        ordering = ['-display_date']
        verbose_name = _('Uutiset')
        verbose_name_plural = _('Uutiset')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title_fi)
        super(Post, self).save(*args, **kwargs)

    def get_hits(self):
        return Tracker.objects.filter(url__endswith=self.slug).count()
