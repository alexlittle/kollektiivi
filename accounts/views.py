
import calendar
import os
import tempfile

from decimal import Decimal
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.core.files import File
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, ListView, FormView

from wkhtmltopdf.views import PDFTemplateView, PDFTemplateResponse

from accounts.models import Transaction, Contract, Config
from accounts.forms import InvoicesForm, CustomInvoiceForm

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

class GetTransactionFileView(TemplateView):

    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        transaction = Transaction.objects.get(pk=id)
        # Construct the full path to the media file
        path = os.path.join(settings.ACCOUNTS_FILES_LOCATION, transaction.file.name)

        # Serve the file
        with open(path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename={filename}'.format(filename=transaction.file.name)
        return response

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

class CustomInvoiceView(FormView):
    template_name = 'accounts/custom_invoice.html'
    form_class = CustomInvoiceForm

    def get(self, request, *args, **kwargs):
        site_tracker.send(sender=None, request=request)
        contract = get_object_or_404(Contract, id=kwargs['id'])
        now = datetime.now()
        next_month = now + relativedelta(months=1)
        self.initial = {
            'to_name': contract.name,
            'to_address': contract.address,
            'to_ytunnus': contract.business_id,
            'invoice_title':  "Palvelupaketti {month}/{year} (service fee)".format(month=next_month.month, year=next_month.year),
            'description_1': "Kuukausmaksu",
            'amount_ex_alv_1': contract.get_monthly_invoice_ex_alv(),
            'amount_alv_rate_1': Config.get("alv_rate")
        }

        form = self.form_class(initial=self.initial)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            total_ex_alv = 0
            total_alv = 0
            total_inc_alv = 0
            invoice_lines = []

            for i in range(1,4):
                if form.cleaned_data['description_{i}'.format(i=i)]:
                    line_amount_ex_alv = Decimal(form.cleaned_data['amount_ex_alv_{i}'.format(i=i)])
                    line_amount_alv = line_amount_ex_alv * Decimal(form.cleaned_data['amount_alv_rate_{i}'.format(i=i)]/100)
                    line_amount_inc_alv = round(line_amount_ex_alv + line_amount_alv,2)
                    invoice_line = {
                        'description': form.cleaned_data['description_{i}'.format(i=i)],
                        'amount_ex_alv': round(line_amount_ex_alv,2),
                        'amount_alv_rate': form.cleaned_data['amount_alv_rate_{i}'.format(i=i)],
                        'amount_inc_alv': line_amount_inc_alv
                    }
                    invoice_lines.append(invoice_line)
                    total_ex_alv = total_ex_alv + line_amount_ex_alv
                    total_alv = total_alv + line_amount_alv
                    total_inc_alv = total_inc_alv + line_amount_inc_alv

            context = {
                'config': Config.get_as_dict(),
                'to_name': form.cleaned_data['to_name'],
                'to_address': form.cleaned_data['to_address'],
                'to_ytunnus': form.cleaned_data['to_ytunnus'],
                'invoice_date': form.cleaned_data['invoice_date'],
                'due_date': form.cleaned_data['due_date'],
                'ref': form.cleaned_data['ref'],
                'invoice_title': form.cleaned_data['invoice_title'],
                'total_ex_alv': round(total_ex_alv,2),
                'total_alv': round(total_alv,2),
                'total_inc_alv': round(total_inc_alv,2),
                'invoice_lines': invoice_lines
            }



            filename = "invoice-{year}-{month}-{name}-{ref}.pdf".format(year=2024,
                                                                        month=5,
                                                                        name=form.cleaned_data['to_name'].lower().replace(" ", "-"),
                                                                        ref=form.cleaned_data['ref'])
            response = PDFTemplateResponse(request=self.request,
                                           filename=filename,
                                           template='accounts/custom_invoice_template.html',
                                           context=context)
            response['Content-Disposition'] = 'inline; filename={filename}'.format(filename=filename)

            # add to transactions
            fp = tempfile.TemporaryFile()
            fp.write(response.rendered_content)

            # save to transactions
            transaction = Transaction()
            transaction.description = "Invoice - {name} - {ref}".format(name=context['to_name'], ref=context['ref'])
            transaction.credit = context['total_inc_alv']
            transaction.sales_tax_charged = context['total_alv']
            transaction.sales_tax_rate = Config.get("alv_rate")
            transaction.file = File(fp, filename)
            transaction.save()
            fp.close()

            return response


        return render(request, self.template_name, {"form": form})
    def form_valid(self, form):
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