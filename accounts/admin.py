from django.contrib import admin

from accounts.models import Transaction, Contract, Config

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'credit', 'debit', 'on_statement')

class ContractAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'start_date', 'end_date', 'meters_sq', 'deposit_held')

class ConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Config, ConfigAdmin)
