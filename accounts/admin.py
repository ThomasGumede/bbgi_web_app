from django.contrib import admin
from accounts.custom_models.account import Account, SubscriptionPackage, SubscriptionOrder

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(SubscriptionPackage)
class SubscriptionPackageAdmin(admin.ModelAdmin):
    pass

@admin.register(SubscriptionOrder)
class SubscriptionOrderAdmin(admin.ModelAdmin):
    pass