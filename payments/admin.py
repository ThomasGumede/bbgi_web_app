from django.contrib import admin
from payments.models import BBGIBankModel, PaymentInformation

@admin.register(BBGIBankModel)
class BBGIBankBankAdmin(admin.ModelAdmin):
    pass

@admin.register(PaymentInformation)
class PaymentInformation(admin.ModelAdmin):
    pass
    
