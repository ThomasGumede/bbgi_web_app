from django.urls import path
from coupons.views import apply_coupon, create_coupon, coupons

app_name = "coupons"
urlpatterns = [
    path("administration/coupons", coupons, name="coupons"),
    path("coupon/apply-coupon", apply_coupon, name="apply-coupon"),
    path("coupon/create-coupon", create_coupon, name="create-coupon")
]

