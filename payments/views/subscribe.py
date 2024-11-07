import json, logging, decimal, requests
from payments.utilities.custom_email import send_subscription_order_received_to_admin
from payments.utilities.yoco_func import headers
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from accounts.models import SubscriptionOrder
from payments.models import PaymentInformation
from payments.tasks import check_payment_update_2_subscription
from coupons.models import Coupon
from django.contrib import messages
from campaigns.utils import PaymentStatus
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site

from payments.utilities.subscription_func import update_payment_status_subscription_order, update_payment_status_zero_balance_subscription_order
from payments.utilities.yoco_func import decimal_to_str

logger = logging.getLogger("payments")

def update_coupon(order_id):
    try:
        coupon = Coupon.objects.get(order_id=order_id, active=True)
        coupon.active = False
        coupon.save(update_fields=["active"])
    except Coupon.DoesNotExist:
        pass

@login_required
def subscription_payment(request, subscription_id):
    subscription_orders = SubscriptionOrder.objects.filter(Q(payment_status=PaymentStatus.NOT_PAID) | Q(payment_status=PaymentStatus.PENDING))
    subscription_order = get_object_or_404(subscription_orders, id=subscription_id, subscriber=request.user)

    
    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse("payments:subscription-payment-success", kwargs={"subscription_id": subscription_order.id}))
        cancel_url = request.build_absolute_uri(reverse("payments:subscription-payment-cancelled", kwargs={"subscription_id": subscription_order.id}))
        fail_url = request.build_absolute_uri(reverse("payments:subscription-payment-failed", kwargs={"subscription_id": subscription_order.id}))
        str_amount = decimal_to_str(subscription_order.total_amount)

        if subscription_order.total_amount == decimal.Decimal(0.00):
            return redirect("payments:subscription-payment-success", subscription_order.id)

        session_data = {
            'successUrl': success_url,
            'cancelUrl': cancel_url,
            "failureUrl": fail_url,
            'amount': int(str_amount),
            'currency': 'ZAR',
            'metadata': {
                "checkoutId": f"{subscription_order.order_id}"
            },
        }

        data = json.dumps(session_data)
        try:
            response = requests.request("POST", "https://payments.yoco.com/api/checkouts", data=data, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            subscription_order.checkout_id = response_data["id"]
            subscription_order.payment_status = PaymentStatus.PENDING
            subscription_order.save(update_fields=["payment_status", "checkout_id"])
            return redirect(response_data["redirectUrl"])

        except requests.ConnectionError as err:
            logger.error(f"Yoco - Connection Error - {err}")
            return render(request, "payments/timeout.html", {"err": err})
        
        except requests.HTTPError as err:
            logger.error(f"Yoco - HTTP Error - {err}")
            return render(request, "payments/error.html", {"message": "Your payment was not processed due to internal error from our payment system, Please try again later"})
        
        except Exception as err:
            logger.error(f"Yoco - Exception - {err}")
            return render(request, "payments/error.html", {"message": "Your payment was not processed due to internal error from our payment system, Please try again later"})

    return render(request, "payments/subscriptions/payment.html", {"subscription_order": subscription_order})

def subscription_payment_failed(request, subscription_id):
    subscription = get_object_or_404(SubscriptionOrder, id=subscription_id)
    subscription.payment_status = PaymentStatus.NOT_PAID
    subscription.save(update_fields=["payment_status"])
    return render(request, "payments/subscriptions/failed.html")

def subscription_payment_cancelled(request, subscription_id):
    subscription = get_object_or_404(SubscriptionOrder, id=subscription_id)
    subscription.delete()
    messages.success(request, "Payment cancelled successfully")
    return redirect("campaigns:campaigns")

@login_required
def subscription_payment_success(request, subscription_id):
    domain = get_current_site(request).domain
    protocol = "https" if request.is_secure() else "http"
    
    subscription = get_object_or_404(SubscriptionOrder, id=subscription_id)
    send_subscription_order_received_to_admin(subscription, request)
    if subscription.total_amount == decimal.Decimal(0.00):
        update_payment_status_zero_balance_subscription_order(request, subscription)
        update_coupon(subscription.id)
        return render(request, "payments/subscriptions/success.html", {"subscription": subscription})

    try:
        payment_information = PaymentInformation.objects.get(id = subscription.checkout_id)
        updated = update_payment_status_subscription_order(json.loads(payment_information.data), request, subscription)

        if updated:
            payment_information.order_number = subscription.order_id
            payment_information.order_updated = True
            update_coupon(subscription.id)
            payment_information.save(update_fields=["order_number", "order_updated"])

        else:
            logger.info(f"something went wrong: check_payment_update_2_subscription.delay((subscription.checkout_id, domain, protocol))")
            check_payment_update_2_subscription.delay(subscription.checkout_id, domain, protocol)
            return render(request, "payments/subscriptions/success.html", {"subscription": subscription})
            

    except PaymentInformation.DoesNotExist as ex:
        logger.info(f"something went wrong: {ex}")
        check_payment_update_2_subscription.delay(subscription.checkout_id, protocol, domain)
        return render(request, "payments/subscriptions/success.html", {"subscription": subscription})        
    
    except Exception as ex:
        logger.error(f"something went wrong: {ex}")
        return render(request, "payments/subscriptions/success.html", {"subscription": subscription})

    return render(request, "payments/subscriptions/success.html", {"subscription": subscription})