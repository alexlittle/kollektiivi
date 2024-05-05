from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required

from accounts.views import AccountsView
app_name = 'accounts'

urlpatterns = [
    path('', staff_member_required(AccountsView.as_view()), name="home"),
    ]

