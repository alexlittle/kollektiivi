from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required

from accounts.views import AccountsView, GenerateContractView
app_name = 'accounts'

urlpatterns = [
    path('', staff_member_required(AccountsView.as_view()), name="home"),
    path('contract/<int:id>/', staff_member_required(GenerateContractView.as_view()), name="generate_contract"),
    ]

