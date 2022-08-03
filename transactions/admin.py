from django.contrib import admin

# Register your models here.

from .models import Transaction, TxIn, TxOut

admin.site.register(Transaction)
admin.site.register(TxIn)
admin.site.register(TxOut)
