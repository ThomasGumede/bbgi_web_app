from django.contrib import admin
from accounts.custom_models.account import Account, SubscriptionPackage, SubscriptionOrder, AboutCompany
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    def profile_image_tag(self, obj):
        """Display user profile image thumbnail in admin."""
        if obj.profile_image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:50%;" />', obj.profile_image.url)
        return _("No Image")

    profile_image_tag.short_description = "Profile Image"

    # Columns in list view
    list_display = (
        "username", "email", "first_name", "last_name", "is_staff", "created", "profile_image_tag"
    )
    list_filter = ("is_staff", "is_superuser", "created")
    search_fields = ("username", "email", "first_name", "last_name", "phone")
    ordering = ("-created",)
    readonly_fields = ("created", "updated", "profile_image_tag",)

    add_fieldsets = (
        ("Personal Info", {
            "fields": (
                "username",
                "first_name",
                "last_name",
                "email",
                "title",
                "profile_image_tag",
                "profile_image",
                "password1",
                "password2",
            ),
        }),
        ("Club Info", {
            "fields": (
                
                "biography",
                
            ),
        }),
        ("Contact & Socials", {
            "fields": (
                "phone",
                "email",
                "facebook",
                "twitter",
                "instagram",
                "linkedIn",
            ),
        }),
        
        ("Permissions", {
            "fields": (

                "is_active",
                "is_staff",
                "is_superuser",
                "is_technical",
                "is_email_activated",
            ),
        }),
        ("Important Dates", {
            "fields": ("last_login", "created", "updated"),
        }),
    )

    # Edit form layout
    fieldsets = (
        ("Personal Info", {
            "fields": (
                "username",
                "first_name",
                "last_name",
                "email",
                "title",
                "profile_image_tag",
                "profile_image",
                
            ),
        }),
        ("Contact & Socials", {
            "fields": (
                "phone",
                
                "facebook",
                "twitter",
                "instagram",
                "linkedIn",
            ),
        }),
        ("Club Info", {
            "fields": (
                "biography",
                "is_technical",
                "is_email_activated",
            ),
        }),
        ("Permissions", {
            "fields": (
                
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        }),
        ("Important Dates", {
            "fields": ("last_login", "created", "updated"),
        }),
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