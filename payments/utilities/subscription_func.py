import logging
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from listings.models import ListingOrder
from campaigns.utils import PaymentStatus
from payments.utilities.custom_email import send_subscription_confirm_email


logger = logging.getLogger("payments")

def update_payment_status_subscription_order(data, request, subscription: ListingOrder):
    try:
        payment_status = PaymentStatus.NOT_PAID

        if data["type"] == "payment.succeeded":
            payment_status = PaymentStatus.PAID
    
        payload = data["payload"]
        payment_method_details = payload["paymentMethodDetails"]
        card_details = payment_method_details.get("card", None)
        subscription.payment_status = payment_status
        subscription.subscription_starts = timezone.now()
        subscription.subscription_ends = timezone.now() + relativedelta(months=12)
        if card_details:
            subscription.payment_method_type = card_details.get("type", "-")
            subscription.payment_method_card_holder = card_details.get("cardHolder", "-")
            subscription.payment_method_masked_card = card_details.get("maskedCard", "-")
            subscription.payment_method_scheme = card_details.get("scheme", "-")

        subscription.payment_date = str(payload.get("createdDate", "-"))
        subscription.save(update_fields=["payment_status", "payment_date", "subscription_starts", "subscription_ends", "payment_method_card_holder", "payment_method_type","payment_method_masked_card", "payment_method_scheme"])

        send_subscription_confirm_email(subscription, request, payment_status)
        return True
    except Exception as ex:
        logger.error(ex)
        return False


def update_payment_status_zero_balance_subscription_order(request, subscription: ListingOrder):
    try:
        
        payment_status = PaymentStatus.PAID
        subscription.subscription_starts = timezone.now()
        subscription.subscription_ends = timezone.now() + relativedelta(months=12)
        subscription.payment_status = payment_status
        subscription.payment_date = str(timezone.now())
        subscription.save(update_fields=["payment_status", "payment_date", "subscription_starts", "subscription_ends"])

        send_subscription_confirm_email(subscription, request, payment_status)
        return True
    except Exception as ex:
        logger.error(ex)
        return False
