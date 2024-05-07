from django.urls import path
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required

from accounts.views import (AccountsView,
                            GenerateContractView,
                            TransactionsView,
                            CreateInvoicesView,
                            TransactionsByMonthView,
                            GetTransactionFileView)
app_name = 'accounts'

urlpatterns = [
    path('', staff_member_required(AccountsView.as_view()), name="home"),
    path('contract/<int:id>/', staff_member_required(GenerateContractView.as_view()), name="generate_contract"),
    path('transaction/file/<int:id>/', staff_member_required(GetTransactionFileView.as_view()), name="get_transaction_file"),
    path('transactions/', staff_member_required(TransactionsView.as_view()), name="transactions_view"),
    path('transactions/<int:year>/<int:month>/',
         staff_member_required(TransactionsByMonthView.as_view()),
         name="transactions_by_month_view"),
    path('invoices/create/', staff_member_required(CreateInvoicesView.as_view()), name="create_invoices"),
    path('invoices/create/done/',
         staff_member_required(TemplateView.as_view(template_name='accounts/create_invoices_done.html')),
         name="create_invoices_done"),
    ]

