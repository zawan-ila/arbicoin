from django.contrib import admin
from transactions.models import Transaction, TransactionOutput, TransactionInput


admin.site.register(Transaction)
admin.site.register(TransactionInput)
admin.site.register(TransactionOutput)
