from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from coupons.forms import CouponApplyForm
from coupons.models import Coupon
import decimal, uuid
from accounts.custom_models.choices import PaymentStatus
from accounts.models import SubscriptionPackage, SubscriptionOrder
from accounts.utilities.company import generate_order_number
from listings.models import Business
from accounts.forms import SubscriptionOrderForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def get_coupon(coupon_id):
    try:
        return Coupon.objects.get(id=uuid.UUID(coupon_id), active=True)
    except Coupon.DoesNotExist:
        return None
    
def apply_order_discount(order: SubscriptionOrder, coupon: Coupon):
    order.discount = coupon.discount
    coupon.order_id = order.id
    coupon.save(update_fields=["order_id"])
    order.save(update_fields=["discount"])

@login_required
def choose_package(request):
    package = SubscriptionPackage.objects.first()
    is_price_droped = False
    
    if package == None:
        messages.warning(request, "Sorry there are currently no subscription packages")
        return redirect("bbgi_home:bbgi-home")
    
    if request.user.subscription != None:
        messages.info(request, "You are already subscribed to our business listing package")
        return redirect("bbgi_home:bbgi-home")
    
    available_order = SubscriptionOrder.objects.filter(Q(payment_status=PaymentStatus.NOT_PAID) | Q(payment_status=PaymentStatus.PENDING) & Q(subscriber=request.user)).first()
    if available_order != None:
        available_order.delete()
    
    return render(request, "accounts/subscriptions/subscribe.html", {"package": package,"price_drop": is_price_droped, "amount": round(package.amount, 2)})

@login_required
def subscribe(request, package_id):
    package = SubscriptionPackage.objects.filter(id=package_id).first()

    if package:
        messages.info(request, "To complete your subscription, we require payment.")
        order = SubscriptionOrder.objects.create(package=package, subscriber=request.user, order_id=generate_order_number(SubscriptionOrder))
        return redirect("accounts:subscription-checkout", order.id)
    else:
        messages.info(request, "Sorry, you cannot subscribe now")
    return redirect("bbgi_home:bbgi-home")

@login_required
def subscription_checkout(request, order_id):
    order = get_object_or_404(SubscriptionOrder, id=order_id, subscriber=request.user)
    form = SubscriptionOrderForm(instance=order)
    form2 = CouponApplyForm()
    coupon_id = request.session.get("coupon_id")
    if coupon_id:
        coupon = get_coupon(coupon_id)
        if coupon:
            apply_order_discount(order, coupon)

    if request.method == "POST":
        form = SubscriptionOrderForm(instance=order, data=request.POST)
        if form.is_valid():
            form.save()
            request.session['coupon_id'] = ''
            messages.success(request, "Billing details successfully saved")
            return redirect("payments:subscription-payment", order.id)
        else:
            messages.error(request, "Please fix errors below")
            return render(request, "accounts/subscriptions/checkout.html", {"form": form, "order": order, "form2": form2})
        
    return render(request, "accounts/subscriptions/checkout.html", {"form": form, "order": order, "form2": form2})

@login_required
def cancel_subscription_order(request, subscription_order_id):
    subscription_order = get_object_or_404(SubscriptionOrder, subscriber = request.user, id = subscription_order_id)
    subscription_order.delete()
    messages.success(request, "Subscription order cancelled!")
    return redirect("bbgi_home:bbgi-home")