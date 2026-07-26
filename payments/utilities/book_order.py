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
# store/services.py

from pathlib import Path
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse


def send_book_order_confirmation_email(
    *,
    order,
    access,
):
    """
    Sends a payment confirmation email to the customer.

    The email includes:
    - HTML order confirmation
    - Secure access link
    - Purchased book attached as a PDF
    """

    book = order.book

    # Generate the access link
    access_path = reverse(
        "store:access",
        kwargs={
            "token": access.token
        }
    )

    access_url = (
        f"{settings.SITE_URL}"
        f"{access_path}"
    )

    # Absolute BBGI logo URL
    logo_url = (
        f"{settings.SITE_URL}"
        "/static/images/logo.png"
    )

    context = {
        "order": order,
        "item": book,
        "access": access,
        "access_url": access_url,
        "logo_url": logo_url,
        "site_url": settings.SITE_URL,
    }

    # Render HTML email
    html_content = render_to_string(
        "emails/store/order-confirmation.html",
        context
    )

    # Plain text fallback
    text_content = f"""
Payment successful!

Hello {order.first_name},

Thank you for your purchase from the BBGI Store.

Your payment has been successfully processed.

Order number:
{order.order_number}

Book:
{book.title}

Access your purchase:
{access_url}

You can also find the purchased book attached to this email.

If you need assistance, please contact BBGI support.

Black Business Growth Initiative
{settings.SITE_URL}
"""

    email = EmailMultiAlternatives(
        subject=(
            f"Payment Successful - "
            f"Order #{order.order_number}"
        ),
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[
            order.email
        ],
    )

    # Attach HTML version
    email.attach_alternative(
        html_content,
        "text/html"
    )

    # Attach the purchased book
    if book.book_file:

        book_file = book.book_file.open(
            "rb"
        )

        try:

            file_name = Path(
                book.book_file.name
            ).name

            email.attach(
                file_name,
                book_file.read(),
                "application/pdf"
            )

        finally:

            book_file.close()

    # Send email
    email.send(
        fail_silently=False
    )

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
     
def send_book_order_confirmation(bookorder_id):
    try:
        bookorder = BookOrder.objecs.get(id=bookorder_id)
    
    except BookOrder.DoesNotExist:
        pass
     
def generate_access_link(bookorder: BookOrder):
    book = bookorder.book