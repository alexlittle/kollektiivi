from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Page(models.Model):
    title = models.CharField(blank=False, max_length=200)
    body = RichTextUploadingField(blank=True, null=True, default=None)
    slug = models.SlugField()
    menu_order_by = models.IntegerField(default=0)
    on_menu = models.BooleanField(default=False)
    on_footer = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['menu_order_by', 'title']
        verbose_name = _('Sivu')
        verbose_name_plural = _('Sivut')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title_fi)
        super(Page, self).save(*args, **kwargs)


class Tag(models.Model):
    name = models.TextField(blank=False, null=False)
    description = RichTextField(blank=True, null=True, default=None)
    slug = models.SlugField()
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name_fi)
        super(Tag, self).save(*args, **kwargs)


class Member(models.Model):
    name = models.CharField(blank=False, max_length=200)
    strapline = models.CharField(blank=True, null=True, default=None, max_length=200)
    body = RichTextUploadingField(blank=True, null=True, default=None)
    slug = models.SlugField()
    order_by = models.IntegerField(default=0)
    photo = models.FileField(upload_to="members", blank=True, default=None)
    active = models.BooleanField(default=False)
    visible = models.BooleanField(default=False)
    contact = RichTextField(blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Jäsen')
        verbose_name_plural = _('Jäseniä')
        ordering = ['order_by', 'name']

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name_fi)
        super(Member, self).save(*args, **kwargs)


class Tracker (models.Model):
    tracker_date = models.DateTimeField(default=timezone.now)
    ip = models.GenericIPAddressField()
    agent = models.TextField(blank=True)
    url = models.TextField(blank=True, null=True, default=None)

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = _('Tracker')
        verbose_name_plural = _('Trackers')
