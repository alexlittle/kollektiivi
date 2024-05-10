import datetime
from django import forms
from dateutil.relativedelta import relativedelta

from accounts.models import Contract


def set_due_date():
    now = datetime.datetime.now()
    due_date = now + relativedelta(day=31)
    return datetime.datetime(due_date.year, due_date.month, due_date.day)

def set_title():
    now = datetime.datetime.now()
    next_month = now + relativedelta(months=1)
    desc = "Palvelupaketti {month}/{year} (service fee)".format(month=next_month.month, year=next_month.year)
    return desc


class InvoicesForm(forms.Form):
    issue_date = forms.CharField(max_length=100, initial=datetime.datetime.now().strftime('%d.%m.%Y') )
    due_date = forms.CharField(max_length=100, initial=set_due_date().strftime('%d.%m.%Y'))
    title = forms.CharField(max_length=100, initial = set_title())
    ref_nos = forms.CharField(max_length=200)
    send_to = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                             queryset=Contract.objects.filter(active=True))
    email = forms.BooleanField(initial=False, required=False)
    email_subject = forms.CharField(max_length=200, required=False)
    email_body = forms.CharField(max_length=500, required=False)


class CustomInvoiceForm(forms.Form):
    to_name = forms.CharField(max_length=100)
    to_address = forms.CharField(max_length=200, required=False)
    to_ytunnus = forms.CharField(max_length=200, required=False)
    invoice_date = forms.CharField(max_length=100, initial=datetime.datetime.now().strftime('%d.%m.%Y'))
    invoice_title = forms.CharField(max_length=200)
    due_date = forms.CharField(max_length=100, initial=datetime.datetime.now().strftime('%d.%m.%Y'))
    ref = forms.CharField(max_length=100)

    description_1 = forms.CharField(max_length=100)
    amount_ex_alv_1 = forms.DecimalField()
    amount_alv_rate_1 = forms.DecimalField()

    description_2 = forms.CharField(max_length=100, required=False)
    amount_ex_alv_2 = forms.DecimalField(required=False)
    amount_alv_rate_2 = forms.DecimalField(required=False)

    description_3 = forms.CharField(max_length=100, required=False)
    amount_ex_alv_3 = forms.DecimalField(required=False)
    amount_alv_rate_3 = forms.DecimalField(required=False)