from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from tinymce.models import HTMLField

class Transaction(models.Model):
    date = models.DateTimeField(default=timezone.now)
    credit = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    debit = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    on_statement = models.BooleanField(blank=False, default=False)
    description = models.CharField(max_length=100, blank=False, null=False)
    sales_tax_charged = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    sales_tax_paid = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    sales_tax_rate = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    file = models.FileField(upload_to="transaction", blank=True, default=None)


class Contract(models.Model):
    name = models.CharField(blank=False, max_length=200)
    email = models.CharField(blank=True, default=None, max_length=200)
    phone = models.CharField(blank=True, default=None, max_length=200)
    address = HTMLField(blank=True, null=True, default=None)
    business_id = models.CharField(blank=True, max_length=20, default=None)
    active = models.BooleanField(blank=False, default=False)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    meters_sq = models.DecimalField(decimal_places=1, max_digits=10, default=0)
    deposit_held = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    contract_doc = models.FileField(upload_to="contract", blank=True, default=None)

class Config(models.Model):
    name = models.CharField(blank=False, max_length=200)
    value = models.CharField(blank=False, max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = _('Config')
        verbose_name_plural = _('Config')

    def __str__(self):
        return self.name

    @staticmethod
    def get_all():
        return Config.objects.all()

    @staticmethod
    def get(name, default=None):
        try:
            return Config.objects.get(name=name).value
        except Config.DoesNotExist:
            return default

    @staticmethod
    def get_int(name, default=None):
        try:
            return int(Config.objects.get(name=name).value)
        except (Config.DoesNotExist, ValueError):
            return default

    @staticmethod
    def update(name, value):
        c, _ = Config.objects.get_or_create(name=name)
        c.value = value
        c.save()