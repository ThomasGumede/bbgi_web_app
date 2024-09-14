from django.contrib import admin
from accounts.custom_models.account import Account, SubscriptionPackage, SubscriptionOrder, AboutCompany

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(AboutCompany)
class AboutCompanyAdmin(admin.ModelAdmin):
    pass

@admin.register(SubscriptionPackage)
class SubscriptionPackageAdmin(admin.ModelAdmin):
    pass

@admin.register(SubscriptionOrder)
class SubscriptionOrderAdmin(admin.ModelAdmin):
    pass