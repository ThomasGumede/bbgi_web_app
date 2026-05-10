from django.contrib import admin
from payments.models import BBGIBankModel, PaymentInformation

@admin.register(BBGIBankModel)
class BBGIBankBankAdmin(admin.ModelAdmin):
    list_display = ('balance', 'order_uuid', 'order_id', 'tip', 'received_at')

@admin.register(PaymentInformation)
class PaymentInformation(admin.ModelAdmin):
    list_display = ('order_number', 'order_updated')
