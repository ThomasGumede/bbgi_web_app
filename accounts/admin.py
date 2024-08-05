from django.contrib import admin
from accounts.custom_models.account import Account, SubscriptionPackage

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(SubscriptionPackage)
class SubscriptionPackageAdmin(admin.ModelAdmin):
    pass