from django.views.generic import TemplateView, ListView

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
        context['contracts'] = Contract.objects.filter(active=True).order_by('name')
        context['transactions'] = Transaction.objects.all().order_by('-date')[:25]
        return context