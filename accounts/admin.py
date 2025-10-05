from django.contrib import admin
from accounts.custom_models.account import Account, SubscriptionPackage, SubscriptionOrder, AboutCompany

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'get_full_name', 'is_active', 'created')
    
    # Add filters on sidebar
    list_filter = ('is_active', 'created')
    readonly_fields = ('id', 'password', 'is_superuser')
    # Search box for fields
    search_fields = ('first_name', 'last_name', 'username', 'email', 'biography')
    
    # Default ordering
    ordering = ('-created',)
    
    # Fields displayed in the form (grouped)
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'username', 'email', 'biography')}),
        ('Advanced options', {'fields': ('is_active',), 'classes': ('collapse',)}),
    )

@admin.register(AboutCompany)
class AboutCompanyAdmin(admin.ModelAdmin):
    pass

@admin.register(SubscriptionPackage)
class SubscriptionPackageAdmin(admin.ModelAdmin):
    pass

@admin.register(SubscriptionOrder)
class SubscriptionOrderAdmin(admin.ModelAdmin):
    pass