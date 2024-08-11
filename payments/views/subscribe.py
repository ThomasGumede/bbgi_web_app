import json, logging
import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from accounts.models import SubscriptionOrder
from payments.models import PaymentInformation
from payments.tasks import check_payment_update_subscription
from django.contrib import messages
from campaigns.utils import PaymentStatus
from payments.utils import headers, decimal_to_str, update_payment_status_subscription_order
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site

logger = logging.getLogger("payments")

@login_required
def subscription_payment(request, subscription_id):
    subscription_order = get_object_or_404(SubscriptionOrder, id=subscription_id, subscriber=request.user, payment_status=PaymentStatus.NOT_PAID)

    
    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse("payments:subscription-payment-success", kwargs={"subscription_id": subscription_order.id}))
        cancel_url = request.build_absolute_uri(reverse("payments:subscription-payment-cancelled", kwargs={"subscription_id": subscription_order.id}))
        fail_url = request.build_absolute_uri(reverse("payments:subscription-payment-failed", kwargs={"subscription_id": subscription_order.id}))
        str_amount = decimal_to_str(subscription_order.total_amount)

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
    return render(request, "payments/subscriptions/cancelled.html")


def subscription_payment_success(request, subscription_id):
    domain = get_current_site(request).domain
    protocol = "https" if request.is_secure() else "http"
    
    subscription = get_object_or_404(SubscriptionOrder, id=subscription_id)
    try:
        payment_information = PaymentInformation.objects.get(id = subscription.checkout_id)
        updated = update_payment_status_subscription_order(json.loads(payment_information.data), request, subscription)

        if updated:
            payment_information.order_number = subscription.order_id
            payment_information.order_updated = True
            payment_information.save(update_fields=["order_number", "order_updated"])

        else:
            check_payment_update_subscription.apply_async((subscription.checkout_id, domain, protocol), countdown=25*60)

    except PaymentInformation.DoesNotExist:
        check_payment_update_subscription.apply_async((subscription.checkout_id, protocol, domain), countdown=25*60)

    return render(request, "payments/subscriptions/success.html", {"subscription": subscription})