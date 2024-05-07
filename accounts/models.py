from decimal import Decimal

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

accounts_storage = FileSystemStorage(location=settings.ACCOUNTS_FILES_LOCATION)

class Transaction(models.Model):
    date = models.DateTimeField(default=timezone.now)
    credit = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    debit = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    on_statement = models.BooleanField(blank=False, default=False)
    description = models.CharField(max_length=100, blank=False, null=False)
    sales_tax_charged = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    sales_tax_paid = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    sales_tax_rate = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    file = models.FileField(storage=accounts_storage, blank=True, default=None)

    @staticmethod
    def get_booked_balance():
        total = Transaction.objects.filter(on_statement=True).aggregate(total=Sum('credit')-Sum('debit'))['total']
        if total:
            return total
        else:
            return 0

    @staticmethod
    def get_pending_balance():
        total = Transaction.objects.filter(on_statement=False).aggregate(total=Sum('credit') - Sum('debit'))['total']
        if total:
            return total
        else:
            return 0

    @staticmethod
    def get_balance_at_date(date):
        trans = Transaction.objects.filter(date__lte=date, on_statement=True).aggregate(credit_sum=Sum("credit"), debit_sum=Sum('debit'))
        if trans['debit_sum'] is None and trans['credit_sum'] is None:
            return 0
        elif trans['debit_sum'] is None:
            return trans['credit_sum']
        elif trans['credit_sum'] is None:
            return trans['debit_sum']
        else:
            return trans['credit_sum'] - trans['debit_sum']

class Contract(models.Model):
    name = models.CharField(blank=False, max_length=200)
    contact_name =  models.CharField(blank=True, default=None, max_length=200)
    email = models.CharField(blank=True, default=None, max_length=200)
    phone = models.CharField(blank=True, default=None, max_length=200)
    address = models.CharField(blank=True, null=True, default=None, max_length=200)
    business_id = models.CharField(blank=True, max_length=20, default=None)
    active = models.BooleanField(blank=False, default=False)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    meters_sq = models.DecimalField(decimal_places=1, max_digits=10, default=0)
    deposit_held = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    contract_doc = models.FileField(storage=accounts_storage, blank=True, default=None)

    def __str__(self):
        return "{name} - {ex_alv} + {alv} = {total}".format(name=self.name,
                                                            ex_alv=self.get_monthly_invoice_ex_alv(),
                                                            alv=self.get_monthly_invoice_alv(),
                                                            total=self.get_monthly_invoice_inc_alv())
    def get_monthly_invoice_ex_alv(self):
        return round(self.meters_sq * Decimal(Config.get('m2_rate_ex_alv', 0)),2)

    def get_monthly_invoice_alv(self):
        return round(self.get_monthly_invoice_ex_alv() * (Decimal(Config.get('alv_rate', 0))/100), 2)

    def get_monthly_invoice_inc_alv(self):
        return self.get_monthly_invoice_ex_alv() + self.get_monthly_invoice_alv()

    @staticmethod
    def get_total_deposit_held():
        return Contract.objects.filter(active=True).aggregate(total=Sum('deposit_held'))['total']

    @staticmethod
    def get_total_m2_rented():
        return Contract.objects.filter(active=True).aggregate(total=Sum('meters_sq'))['total']

    @staticmethod
    def get_total_monthly_invoices_ex_alv():
        m2_rate = Decimal(Config.get('m2_rate_ex_alv', 0))
        return Contract.get_total_m2_rented() * m2_rate

    @staticmethod
    def get_total_monthly_invoices_inc_alv():
        return Contract.get_total_monthly_invoices_ex_alv() * (1+(Decimal(Config.get('alv_rate', 0))/100))

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
    def get_as_dict():
        config = {}
        for c in Config.get_all():
            config[c.name] = c.value
        return config

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