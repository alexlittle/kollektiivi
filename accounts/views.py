import datetime
import os
from decimal import Decimal

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
        context['funds_pending'] = 0
        context['total_m2_rented'] = Contract.get_total_m2_rented()
        context['total_monthly_invoices_ex_alv'] = Contract.get_total_monthly_invoices_ex_alv()
        context['total_monthly_invoices_inc_alv'] = Contract.get_total_monthly_invoices_inc_alv()
        context['contracts'] = Contract.objects.filter(active=True).order_by('name')
        context['transactions'] = Transaction.objects.filter(on_statement=False).order_by('-date')
        return context

class TransactionsView(ListView):

    template_name = 'accounts/transactions.html'

    def get(self, request, *args, **kwargs):
        site_tracker.send(sender=None, request=request)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = Transaction.objects.all().order_by('-date')
        return qs

class CreateInvoicesView(FormView):

    template_name = 'accounts/create_invoices.html'
    form_class = InvoicesForm
    success_url = "done/"

    def form_valid(self, form):
        invoice_date = form.cleaned_data['issue_date']
        due_date = form.cleaned_data['due_date']
        title = form.cleaned_data['title']
        send_to_ids = form.cleaned_data['send_to']
        ref_nos = form.cleaned_data['ref_nos'].split(',')
        template = 'accounts/invoice_template.html'

        tempdate = datetime.datetime.strptime(due_date, "%d.%m.%Y").date()
        year = tempdate.year
        month = '{:02d}'.format(tempdate.month)
        for idx, invoice in enumerate(send_to_ids):

            print(invoice)
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
                                                                        name=invoice.name.lower(),
                                                                        ref=ref_nos[idx])
            output_path = os.path.join('/home/alex/Downloads', filename)
            with open(output_path, "wb") as f:
                f.write(response.rendered_content)

            # save to transactions

            # email to user
            '''
            response = PDFTemplateResponse(request=self.request,
                                           filename="invoice.pdf",
                                           template=template,
                                           context=context)

            filename = "invoice-{year}-{month}-{name}-{ref}.pdf".format(year=year,
                                                                        month=month,
                                                                        name=invoice.name.lower(),
                                                                        ref=ref_nos[idx])
            output_path = os.path.join(settings.INVOICE_OUTPUT_DIR, filename)
            with open(output_path, "wb") as f:
                f.write(response.rendered_content)

            return render(self.request, template, context)
            '''
            return render(self.request, template, context)
        #return super().form_valid(form)


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