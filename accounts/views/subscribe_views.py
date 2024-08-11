from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import decimal, uuid
from accounts.custom_models.choices import PaymentStatus
from accounts.models import SubscriptionPackage, SubscriptionOrder
from accounts.utilities.company import generate_order_number
from listings.models import Business
from django.contrib.auth.decorators import login_required

@login_required
def choose_package(request):
    package = SubscriptionPackage.objects.first()
    businesses = Business.objects.count()
    is_price_droped = False
    if businesses < 50:
        is_price_droped = True
    if package == None:
        messages.warning(request, "Sorry there are currently no subscription packages")
        return redirect("bbgi_home:bbgi-home")
    
    if request.user.subscription != None:
        messages.info(request, "You are already subscribed to our business listing package")
        return redirect("bbgi_home:bbgi-home")
    
    if is_price_droped: 
        amount = decimal.Decimal(package.amount) - (decimal.Decimal(package.amount) * decimal.Decimal((80/100)))
    
    return render(request, "accounts/subscriptions/subscribe.html", {"package": package,"price_drop": is_price_droped, "amount": amount})

@login_required
def subscribe(request, package_id):
    package = SubscriptionPackage.objects.filter(id=package_id).first()
    businesses = Business.objects.count()
    is_price_droped = False
    if businesses < 50:
        is_price_droped = True
    
    
    if package:
        available_order = SubscriptionOrder.objects.filter(package=package, subscriber=request.user, payment_status=PaymentStatus.NOT_PAID).first()
        if available_order:
            messages.info(request, "To complete your subscription, we require payment.")
            return redirect("payments:subscription-payment", available_order.id)
        else:
            amount = package.amount
            if is_price_droped: 
                amount = decimal.Decimal(package.amount) - (decimal.Decimal(package.amount) * decimal.Decimal((80/100)))
            messages.info(request, "To complete your subscription, we require payment.")
            vat = decimal.Decimal(amount) * decimal.Decimal((15/100))
            order = SubscriptionOrder.objects.create(package=package, subscriber=request.user, total_amount=amount, vat=vat, order_id=generate_order_number(SubscriptionOrder))
            return redirect("payments:subscription-payment", order.id)
    return redirect("bbgi_home:bbgi-home")

@login_required
def cancel_subscription_order(request, subscription_order_id):
    subscription_order = get_object_or_404(SubscriptionOrder, subscriber = request.user, id = subscription_order_id)
    subscription_order.delete()
    messages.success(request, "Subscription order cancelled!")
    return redirect("bbgi_home:bbgi-home")