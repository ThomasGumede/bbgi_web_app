from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from coupons.forms import CouponApplyForm
from coupons.models import Coupon
import decimal, uuid
from accounts.custom_models.choices import PaymentStatus
from listings.models import ListingOrder, Business
from accounts.utilities.company import generate_order_number
from listings.forms import ListingOrderForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def get_coupon(coupon_id):
    try:
        return Coupon.objects.get(id=uuid.UUID(coupon_id), active=True)
    except Coupon.DoesNotExist:
        return None
    
def apply_order_discount(order: ListingOrder, coupon: Coupon):
    order.discount = coupon.discount
    coupon.order_id = order.id
    coupon.save(update_fields=["order_id"])
    order.save(update_fields=["discount"])

@login_required
def order_subscription(request, listing_slug):
    listing = get_object_or_404(Business, slug=listing_slug, owner=request.user)
    listing_order = ListingOrder.objects.filter(listing=listing).first()
    if listing_order == None:

        listing_order= ListingOrder.objects.create(listing=listing, subscriber=request.user, order_id=generate_order_number(ListingOrder))
    

    form2 = CouponApplyForm()
    form = ListingOrderForm(instance=listing_order)
    coupon_id = request.session.get("coupon_id")
    if coupon_id:
        coupon = get_coupon(coupon_id)
        if coupon:
            apply_order_discount(listing_order, coupon)

    if request.method == "POST":
        form = ListingOrderForm(instance=listing_order, data=request.POST)
        if form.is_valid():
            form.save() 
            request.session['coupon_id'] = ''
            messages.success(request, "Billing details successfully saved")
            return redirect("payments:subscription-payment", listing_order.id)
        else:
            messages.error(request, "Please fix errors below")
            
        
    return render(request, "business/order/checkout.html", {"form": form, "order": listing_order, "form2": form2})

@login_required
def cancel_listing_order(request, order_id):
    listing_order = ListingOrder.objects.filter(id=order_id).first()
    if listing_order:
        listing_order.listing.delete()
        listing_order.delete()

    messages.success(request, "Business listing successfully cancelled")
    return redirect("listings:get-started-with-listing")