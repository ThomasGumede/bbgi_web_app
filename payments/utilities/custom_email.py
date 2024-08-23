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
    try:
        # Render invoice to PDF
        invoice_template = get_template("emails/tickets/invoice.html")
        invoice_context = {
            "buyer_full_name": order.buyer.get_full_name(),
            "order": order,
            "due_date": reservation_time(),
        }
        render_invoice = invoice_template.render(invoice_context, request=request)
        pdf_file = HTML(string=render_invoice).write_pdf()
        
        # Save PDF to order's receipt
        buffer = BytesIO(pdf_file)
        order.receipt.save(f'{order.order_number}_invoice.pdf', buffer)
        
        # Prepare files for email attachments
        files = [{"file_content": base64.b64encode(pdf_file).decode(), "filename": f'{order.order_number}_invoice.pdf'}]

        context = {
            "user": order.buyer.get_full_name(),
            "order": order,
        }

        if status == "payment.succeeded" or status == PaymentStatus.PAID:
            mail_subject = f"Your tickets for {order.event.title} on {order.event.date_time_formatter()}"
            message_template = "emails/tickets/ticket-order-email.html"
            
            with open(order.tickets_pdf_file.path, 'rb') as pdf_file:
                pdf_content = pdf_file.read()
                encoded_content = base64.b64encode(pdf_content).decode()
                files.append({"file_content": encoded_content, "filename": f'{order.order_number}_tickets.pdf'})
        else:
            mail_subject = f"Your tickets order for {order.event.title} on {order.event.date_time_formatter()} was cancelled"
            message_template = "emails/tickets/order-cancelled.html"

        # Render email content
        message = render_to_string(message_template, context, request=request)

        # Send email with attachments
        sent = send_html_email_with_attachments(order.buyer.email, mail_subject, message, "BBGI Events <events@bbgi.co.za>", files)
        
        if not sent:
            email_logger.error(f"Failed to send tickets email to {order.buyer.email} for order number {order.order_number}")
            return False

        return True

    except Exception as ex:
        email_logger.error(f"Error in sending ticket email: {ex}")
        return False
  
def send_contribution_confirm_email(order: ContributionModel, request, status):
    try:
        # Render invoice to PDF
        template = get_template("emails/contributions/invoice-contribution.html")
        rendered_template = template.render({
            "buyer_full_name": order.contributor.get_full_name(),
            "order": order,
            "due_time": in_fourteen_days()
        }, request=request)
        
        pdf_file = HTML(string=rendered_template).write_pdf()
        buffer = BytesIO(pdf_file)
        order.receipt.save(f'{order.order_number}_invoice.pdf', buffer)
        
        # Prepare files for email attachments
        files = [{"file_content": base64.b64encode(pdf_file).decode(), "filename": f'{order.order_number}_invoice.pdf'}]
        context = {
            "user": order.contributor.get_full_name(),
            "order": order
        }

        if status == "payment.succeeded" or status == PaymentStatus.PAID:
            mail_subject = f"Your contribution confirmation for {order.campaign.title} campaign was successful"
            message_template = "emails/contributions/contribution-email.html"
        else:
            mail_subject = f"Your contribution payment for {order.campaign.title} campaign was unsuccessful"
            message_template = "emails/contributions/contribution-cancelled.html"

        # Render email content
        message = render_to_string(message_template, context, request=request)

        # Send email with attachments
        sent = send_html_email_with_attachments(order.contributor.email, mail_subject, message, "BBGI Campaigns <orders@bbgi.co.za>", files)
        
        if not sent:
            email_logger.error(f"Failed to send confirmation email for order {order.order_number} to {order.contributor.email}")
            return False

        return True

    except Exception as ex:
        email_logger.error(f"Error in sending contribution confirmation email: {ex}")
        return False

def send_subscription_confirm_email(order: SubscriptionOrder, request, status):
    try:
        context = {
            "user": order.subscriber.get_full_name(),
            "order": order
        }

        if status == "payment.succeeded" or status == PaymentStatus.PAID:
            mail_subject = "BBGI Payment Received"
            message_template = "emails/subscription/payment_received.html"
        else:
            mail_subject = f"Your contribution payment for {order.campaign.title} campaign was unsuccessful"
            message_template = "emails/subscription/payment_cancelled.html"

        # Render email content
        message = render_to_string(message_template, context, request=request)

        # Send email
        sent = send_html_email_with_attachments(order.subscriber.email, mail_subject, message, "BBGI <bbgiorders@bbgi.co.za>")

        if not sent:
            email_logger.error(f"Failed to send subscription confirmation email for order {order.order_number} to {order.subscriber.email}")
            return False

        return True

    except Exception as ex:
        email_logger.error(f"Error in sending subscription confirmation email: {ex}")
        return False



