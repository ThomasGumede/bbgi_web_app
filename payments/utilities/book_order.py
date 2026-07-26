import logging
from celery import shared_task
from django.utils import timezone
from campaigns.utils import PaymentStatus
from payments.ordermodels.storeorder import BookOrder
from django.template.loader import render_to_string
from django.template.loader import get_template
from weasyprint import HTML
from django.core.mail import EmailMessage
from django.conf import settings

logger = logging.getLogger('payments')

def confirm_book_order(data, request,  bookorder: BookOrder):
    try:
        if data["type"] == "payment.succeeded":
            payment_status = PaymentStatus.PAID
            payload = data["payload"]
            payment_method_details = payload["paymentMethodDetails"]
            card_details = payment_method_details.get("card", None)
            bookorder.paid = True
            bookorder.status = payment_status
            if card_details:
                bookorder.payment_method_type = card_details.get("type", "-")
                bookorder.payment_method_card_holder = card_details.get("cardHolder", "-")
                bookorder.payment_method_masked_card = card_details.get("maskedCard", "-")
                bookorder.payment_method_scheme = card_details.get("scheme", "-")

            bookorder.payment_date = str(payload.get("createdDate", "-"))
            bookorder.save(update_fields=['paid', 'status', 'payment_date', 'payment_method_type', 'payment_method_card_holder', 'payment_method_scheme', 'payment_method_masked_card'])
            
        else:
            payment_status = PaymentStatus.NOT_PAID
            bookorder.paid = True
            bookorder.status = payment_status
            
    except Exception as ex:
         logger.error(ex)
         return False