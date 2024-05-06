from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView

from wkhtmltopdf.views import PDFTemplateView

from accounts.models import Transaction, Contract, Config
from kollektiivi.signals import site_tracker



class AccountsView(TemplateView):

    template_name = 'accounts/index.html'

    def get(self, request, *args, **kwargs):
        site_tracker.send(sender=None, request=request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['funds_booked_balance'] = 0
        context['funds_available'] = 0
        context['deposit_balance'] = 0
        context['total_deposit_held'] = Contract.get_total_deposit_held()
        context['total_m2_rented'] = Contract.get_total_m2_rented()
        context['total_monthly_invoices_ex_alv'] = Contract.get_total_monthly_invoices_ex_alv()
        context['total_monthly_invoices_inc_alv'] = Contract.get_total_monthly_invoices_inc_alv()
        context['contracts'] = Contract.objects.filter(active=True).order_by('name')
        context['transactions'] = Transaction.objects.all().order_by('-date')[:25]
        return context


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