from django.contrib import admin
from coupons.models import Coupon

@admin.action(description="Deactivate selected coupons")
def make_inactive(modeladmin, request, querset):
    querset.update(active=False)

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "discount", "valid_from", "valid_to", "active")
    list_filter = ("active", "valid_from", "valid_to")
    actions = [make_inactive]
