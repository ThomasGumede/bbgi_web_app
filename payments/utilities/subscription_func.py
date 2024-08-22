import logging
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from accounts.custom_models.account import SubscriptionOrder
from campaigns.utils import PaymentStatus
from payments.utilities.custom_email import send_subscription_confirm_email


logger = logging.getLogger("payments")

def update_payment_status_subscription_order(data, request, subscription: SubscriptionOrder):
    try:
        payment_status = PaymentStatus.NOT_PAID

        if data["type"] == "payment.succeeded":
            payment_status = PaymentStatus.PAID
            if subscription.subscriber:
                subscription.subscriber.subscription = subscription.package
                subscription.subscriber.is_paid = True
                subscription.subscriber.subscription_starts = timezone.now()
                subscription.subscriber.subscription_ends = timezone.now() + relativedelta(months=12)
                subscription.subscriber.save(update_fields=["subscription", "is_paid", "subscription_starts", "subscription_ends"])
        payload = data["payload"]
        payment_method_details = payload["paymentMethodDetails"]
        card_details = payment_method_details.get("card", None)
        subscription.payment_status = payment_status
        if card_details:
            subscription.payment_method_type = card_details.get("type", "-")
            subscription.payment_method_card_holder = card_details.get("cardHolder", "-")
            subscription.payment_method_masked_card = card_details.get("maskedCard", "-")
            subscription.payment_method_scheme = card_details.get("scheme", "-")

        subscription.payment_date = str(payload.get("createdDate", "-"))
        subscription.save(update_fields=["payment_status", "payment_method_card_holder", "payment_method_type","payment_method_masked_card", "payment_method_scheme"])

        send_subscription_confirm_email(subscription, request, payment_status)
        return True
    except Exception as ex:
        return False

