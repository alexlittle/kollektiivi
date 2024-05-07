
import calendar
import tempfile
from decimal import Decimal
from datetime import datetime, timedelta

from django.core.files import File
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, ListView, FormView

from wkhtmltopdf.views import PDFTemplateView, PDFTemplateResponse

from accounts.models import Transaction, Contract, Config
from accounts.forms import InvoicesForm

from kollektiivi.signals import site_tracker


class AccountsView(TemplateView):

    template_name = 'accounts/index.html'

    def get(self, request, *args, **kwargs):
        site_tracker.send(sender=None, request=request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deposit_balance'] = Contract.get_total_deposit_held() - Decimal(Config.get("vr_deposit"))
        context['funds_booked_balance'] = Transaction.get_booked_balance()
        context['funds_available'] = context['funds_booked_balance'] - context['deposit_balance']
        context['funds_pending'] = Transaction.get_pending_balance()
        context['total_deposit_held'] = Contract.get_total_deposit_held()
        context['total_m2_rented'] = Contract.get_total_m2_rented()
        context['total_monthly_invoices_ex_alv'] = Contract.get_total_monthly_invoices_ex_alv()
        context['total_monthly_invoices_inc_alv'] = Contract.get_total_monthly_invoices_inc_alv()
        context['contracts'] = Contract.objects.filter(active=True).order_by('name')
        context['pending_transactions'] = Transaction.objects.filter(on_statement=False).order_by('-date')
        context['transaction_months'] = Transaction.objects.filter(on_statement=True).dates('date', 'month', order='DESC')
        return context

class TransactionsView(ListView):

    template_name = 'accounts/transactions.html'
    paginate_by = 50

    def get(self, request, *args, **kwargs):
        site_tracker.send(sender=None, request=request)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = Transaction.objects.all().order_by('-date')
        return qs


class TransactionsByMonthView(TemplateView):

    template_name = 'accounts/transactions_by_month.html'

    def get(self, request, *args, **kwargs):
        site_tracker.send(sender=None, request=request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = kwargs['year']
        month = kwargs['month']

        consulting = Transaction.objects.filter(date__month=month, date__year=year, on_statement=True).order_by('date')

        data = []

        for c in consulting:
            obj = {'transaction': c, 'balance': Transaction.get_balance_at_date(c.date)}
            data.append(obj)

        start_date = datetime(year, month, 1, 23, 59, 59) - timedelta(days=1)
        end_date = datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)

        opening_balance = Transaction.get_balance_at_date(start_date)
        closing_balance = Transaction.get_balance_at_date(end_date)

        totals = consulting.aggregate(total_credit=Sum("credit"),
                                      total_debit=Sum("debit"),
                                      total_alv_charged=Sum('sales_tax_charged'),
                                      total_alv_paid=Sum('sales_tax_paid'))

        context['data'] = data
        context['opening_balance'] = opening_balance
        context['closing_balance'] = closing_balance
        context['start_date'] = datetime(year, month, 1)
        context['end_date'] = end_date
        context['totals'] = totals

        if end_date.month == datetime.now().month and end_date.year == datetime.now().year:
            context['deposit_balance'] = Contract.get_total_deposit_held() - Decimal(Config.get("vr_deposit"))
            context['funds_available'] = closing_balance - context['deposit_balance']

        return context

class CreateInvoicesView(FormView):

    template_name = 'accounts/create_invoices.html'
    form_class = InvoicesForm
    success_url = "done/"

    def get(self, request, *args, **kwargs):
        site_tracker.send(sender=None, request=request)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        invoice_date = form.cleaned_data['issue_date']
        due_date = form.cleaned_data['due_date']
        title = form.cleaned_data['title']
        send_to_ids = form.cleaned_data['send_to']
        ref_nos = form.cleaned_data['ref_nos'].split(',')
        template = 'accounts/invoice_template.html'

        tempdate = datetime.strptime(due_date, "%d.%m.%Y").date()
        year = tempdate.year
        month = '{:02d}'.format(tempdate.month)
        for idx, invoice in enumerate(send_to_ids):

            context = {
                'invoice_date': invoice_date,
                'due_date': due_date,
                'title': title,
                'ref': ref_nos[idx],
                'invoice_info': invoice,
                'config': Config.get_as_dict()
            }

            # create pdf invoice
            response = PDFTemplateResponse(request=self.request,
                                           filename="invoice.pdf",
                                           template=template,
                                           context=context)

            filename = "invoice-{year}-{month}-{name}-{ref}.pdf".format(year=year,
                                                                        month=month,
                                                                        name=invoice.name.lower().replace(" ","-"),
                                                                        ref=ref_nos[idx])
            fp = tempfile.TemporaryFile()
            fp.write(response.rendered_content)

            # save to transactions
            transaction = Transaction()
            transaction.description = "Invoice - {name} - {ref}".format(name=invoice.name, ref=ref_nos[idx])
            transaction.credit = invoice.get_monthly_invoice_inc_alv()
            transaction.sales_tax_charged = invoice.get_monthly_invoice_alv()
            transaction.sales_tax_rate = Config.get("alv_rate")
            transaction.file = File(fp, filename)
            transaction.save()
            fp.close()

            # email to user


        return super().form_valid(form)


class GenerateContractView(PDFTemplateView):

    template_name = 'accounts/contract_template.html'
    cmd_options = {'encoding': 'utf8',
                   "enable-local-file-access": "",
                   "margin-top": "15",
                   "margin-right": "15",
                   "margin-bottom": "15",
                   "margin-left": "15",
                   "footer-right": "[page]/[topage]"}
    def get(self, request, *args, **kwargs):
        site_tracker.send(sender=None, request=request)
        self.object = get_object_or_404(Contract, id=kwargs['id'])
        return super().get(request, *args, **kwargs)

    def get_filename(self):
        name = self.object.name.lower().replace(" ", "-")
        return "contract-{name}.pdf".format(name=name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contract'] = self.object
        context['config'] = Config.get_as_dict()
        return context