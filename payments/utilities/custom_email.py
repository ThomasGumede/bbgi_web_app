import hashlib
import base64
import hmac, logging, decimal
from accounts.custom_models.account import SubscriptionOrder
from accounts.utilities.custom_email import send_html_email_with_attachments
from events.models import TicketOrderModel, reservation_time
from campaigns.models import ContributionModel, in_fourteen_days
from campaigns.utils import PaymentStatus
from events.models import TicketOrderModel
from io import BytesIO
from django.template.loader import render_to_string
from django.template.loader import get_template
from weasyprint import HTML
email_logger = logging.getLogger("emails")

def send_tickets_email(status, order: TicketOrderModel, request):
    
    invoice = get_template("emails/tickets/invoice.html")
    render_invoice = invoice.render({
            "buyer_full_name": order.buyer.get_full_name(),
            "order": order,
            "due_date": reservation_time(),
                
        }, request=request)
        
    pdf_file = HTML(string=render_invoice).write_pdf()
    files = [
            {"file_content": base64.b64encode(pdf_file).decode(), "name": f'{order.order_number}_invoice.pdf'}
        ]
        
    context = {
                "user": order.buyer.get_full_name(),
                "order": order
            }
    if status == "payment.succeeded" or status == PaymentStatus.PAID:

        mail_subject = f"Your tickets for {order.event.title} on {order.event.date_time_formatter()}"
        message = render_to_string("emails/tickets/ticket-order-email.html", context, request=request
            )
                    
        with open(order.tickets_pdf_file.path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()

        encoded_content = base64.b64encode(pdf_content).decode()
        
        files.append({"file_content": encoded_content, "name": f'{order.order_number}_tickets.pdf'})

    else:
        mail_subject = f"Your tickets order for {order.event.title} on {order.event.date_time_formatter()} was cancelled"
        message = render_to_string("emails/tickets/order-cancelled.html", context,
            )

    sent = send_html_email_with_attachments(order.buyer.email, mail_subject, message, "Ndwandwa Fam Events <events@ndwandwa.africa>", files)
            
    if not sent:
        email_logger.error(f"Trouble sending tickets email to {order.buyer.email} order number {order.order_number}")
        return False
        
    return True
    
def send_contribution_confirm_email(order: ContributionModel, request, status):

    template = get_template("emails/contributions/invoice-contribution.html")
    rendered_template = template.render({
            "buyer_full_name": order.contributor.get_full_name(),
            "order": order,
            "due_time": in_fourteen_days()
        }, request=request)

    pdf_file = HTML(string=rendered_template).write_pdf()
    buffer = BytesIO(pdf_file)
    files = [
            {"file_content": base64.b64encode(pdf_file).decode(), "name": f'{order.order_number}_invoice.pdf'}
        ]
    context = {
                "user": order.contributor.get_full_name(),
                "order": order
            }

    if status == "payment.succeeded" or status == PaymentStatus.PAID:
        mail_subject = F"Your contribution confirmation {order.campaign.title} campaign was successful"
        message = render_to_string("emails/contributions/contribution-email.html",
                    context, request=request
                )
    else:
        mail_subject = F"Your contribution payment {order.campaign.title} campaign was unsuccessful"
        message = render_to_string("emails/contributions/contribution-cancelled.html",
                    context,
                )

    sent = send_html_email_with_attachments(order.contributor.email, mail_subject, message, "Ndwandwa Campaigns <campaigns@ndwandwa.africa>", files)
          
    if not sent:
        email_logger.error(f"confirmation email not sent for {order.order_number} to {order.contributor.email}")
        return False
            
    return True

def send_subscription_confirm_email(order: SubscriptionOrder, request, status):

    try:
        context = {
                    "user": order.subscriber.get_full_name(),
                    "order": order
                }

        if status == "payment.succeeded" or status == PaymentStatus.PAID:
            mail_subject = F"BBGI Payment Received"
            message = render_to_string("emails/subscriptions/payment_received.html",
                        context, request=request
                    )
        else:
            mail_subject = F"Your contribution payment {order.campaign.title} campaign was unsuccessful"
            message = render_to_string("emails/subscriptions/payment_cancelled.html",
                        context,
                    )

        sent = send_html_email_with_attachments(order.subscriber.email, mail_subject, message, "BBGI <bbgiorders@bbgi.co.za>")
            
        if not sent:
            email_logger.error(f"confirmation email not sent for {order.order_number} to {order.contributor.email}")
            return False
                
        return True
    except Exception as ex:
        email_logger.error(ex)
        return False
