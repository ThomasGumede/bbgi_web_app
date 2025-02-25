from accounts.utilities.custom_email import send_html_email_with_attachments
from payments.utilities.custom_email import send_ticket_order_received_to_admin, send_tickets_email
from payments.utilities.yoco_func import headers
import requests, logging, json, decimal, base64
from accounts.custom_models.account import SubscriptionOrder
from accounts.utilities.custom_email import send_html_email_with_attachments, send_html_email
from events.models import TicketOrderModel, reservation_time
from campaigns.models import ContributionModel, in_fourteen_days
from campaigns.utils import PaymentStatus
from events.models import TicketOrderModel
from io import BytesIO
from django.template.loader import render_to_string
from django.template.loader import get_template
from weasyprint import HTML
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from coupons.models import Coupon
from events.models import TicketOrderModel
from campaigns.utils import PaymentStatus
from payments.models import PaymentInformation
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from payments.tasks import resend_tickets_2_task, check_payment_update_2_ticket_order
from django.contrib.sites.shortcuts import get_current_site

from payments.utilities.ticket_func import update_payment_status_ticket_order, update_payment_status_zero_balance_ticket_order
from payments.utilities.yoco_func import decimal_to_str
from django.template.loader import render_to_string
from accounts.utilities.company import COMPANY



logger = logging.getLogger("tasks")
email_logger = logging.getLogger("emails")

logger = logging.getLogger("payments")

def update_coupon(coupon_code) -> None:
    try:
        coupon = Coupon.objects.get(code=coupon_code, active=False)
        coupon.active = True
        coupon.save(update_fields=["active"])
    except Coupon.DoesNotExist:
        pass

@login_required
def payment(request, ticket_order_id):
    ticket_orders_queryset = TicketOrderModel.objects.filter(paid = PaymentStatus.NOT_PAID, buyer=request.user)
    ticket_order = get_object_or_404(ticket_orders_queryset, id=ticket_order_id)
    
    if request.method == 'POST':
        
        success_url = request.build_absolute_uri(reverse("payments:ticket-payment-success", kwargs={"ticket_order_id": ticket_order.id}))
        cancel_url = request.build_absolute_uri(reverse("payments:ticket-payment-cancelled", kwargs={"ticket_order_id": ticket_order.id}))
        fail_url = request.build_absolute_uri(reverse("payments:ticket-payment-failed", kwargs={"ticket_order_id": ticket_order.id}))
        str_amount = decimal_to_str(ticket_order.total_price)

        if ticket_order.total_price == decimal.Decimal(0.00):
            return redirect("payments:ticket-payment-success", ticket_order.id)
        
        lineitems = []
        for ticket in ticket_order.tickets.all():
            lineitems.append(
                {
                    "displayName": ticket.ticket_type.title,
                    "quantity": ticket.quantity,
                    "pricingDetails": {
                        "price": int(decimal_to_str(ticket.ticket_type.price))
                    }
                }
            )

        session_data = {
            'successUrl': success_url,
            'cancelUrl': cancel_url,
            "failureUrl": fail_url,
            'amount': int(str_amount),
            'currency': 'ZAR',
            'metadata': {
                "checkoutId": f"{ticket_order.order_number}"
            },
            "lineItems": lineitems

        }
        data = json.dumps(session_data)
        try:
            response = requests.request("POST", "https://payments.yoco.com/api/checkouts", data=data, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            ticket_order.checkout_id = response_data["id"]
            ticket_order.paid = PaymentStatus.PENDING
            ticket_order.save(update_fields=["paid", "checkout_id"])
            return redirect(response_data["redirectUrl"])

        except requests.ConnectionError as err:
            return render(request, "payments/timeout.html", {"err": err})
        
        except requests.HTTPError as err:
            logger.error(f"Yoco - {err}")
            return render(request, "payments/error.html", {"message": "Your payment was not processed due to internal error from our payment system, Please try again later"})
        
        except Exception as err:
            logger.error(f"Yoco - {err}")
            return render(request, "payments/error.html", {"message": "Your payment was not processed due to internal error from our payment system, Please try again later"})

    return render(request, "payments/tickets/payment.html", {"ticketorder": ticket_order, "mode": "payment"})

@login_required
def tickets_payment_success(request, ticket_order_id):
    
    domain = get_current_site(request).domain
    protocol = "https" if request.is_secure() else "http"
    ticket_order = get_object_or_404(TicketOrderModel, id=ticket_order_id, buyer=request.user)
    notified_admin = send_ticket_order_received_to_admin(ticket_order, request)
    if ticket_order.total_price == decimal.Decimal(0.00):
        updated = update_payment_status_zero_balance_ticket_order(request, ticket_order)
        return render(request, "payments/tickets/success.html", {"ticketorder": ticket_order})
    
    if ticket_order.paid == PaymentStatus.PENDING:
        try:
            payment_information = PaymentInformation.objects.get(id = ticket_order.checkout_id)
            updated = update_payment_status_ticket_order(json.loads(payment_information.data), request, ticket_order)

            if updated:
                payment_information.order_number = ticket_order.order_number
                payment_information.order_updated = True
                update_coupon(ticket_order.coupon_code)
                payment_information.save(update_fields=["order_number", "order_updated"])
            else:
               check_payment_update_2_ticket_order.delay(ticket_order.checkout_id, protocol, domain)
               return render(request, "payments/tickets/success.html", {"ticketorder": ticket_order})

        except PaymentInformation.DoesNotExist as ex:
            logger.error(f"Payment error - {ex}")
            check_payment_update_2_ticket_order.delay(ticket_order.checkout_id, protocol, domain)
            return render(request, "payments/tickets/success.html", {"ticketorder": ticket_order})
        
        except Exception as ex:
            logger.error(f"something went wrong: {ex}")
            return render(request, "payments/tickets/success.html", {"ticketorder": ticket_order})
    
    
    return render(request, "payments/tickets/success.html", {"ticketorder": ticket_order})

@login_required
def verify_ticket_payment_order(request, ticket_order_id):
    domain = get_current_site(request).domain
    protocol = "https" if request.is_secure() else "http"
    ticket_order = get_object_or_404(TicketOrderModel, id=ticket_order_id)
    if ticket_order.paid == PaymentStatus.PENDING:
        try:
            payment_information = PaymentInformation.objects.get(id = ticket_order.checkout_id)
            updated = update_payment_status_ticket_order(json.loads(payment_information.data), request, ticket_order)

            if updated:
                payment_information.order_number = ticket_order.order_number
                payment_information.order_updated = True
                update_coupon(ticket_order.coupon_code)
                payment_information.save(update_fields=["order_number", "order_updated"])
            else:
               check_payment_update_2_ticket_order.delay(ticket_order.checkout_id, protocol, domain)

        except PaymentInformation.DoesNotExist as ex:
            logger.error(f"Payment error - {ex}")
            check_payment_update_2_ticket_order.delay(ticket_order.checkout_id, protocol, domain)
            return render(request, "payments/tickets/verify-payment.html", {"ticketorder": ticket_order})
    else:
        try:
            # Render invoice to PDF
            invoice_template = get_template("emails/tickets/invoice_v2.html")
            invoice_context = {
                "buyer_full_name": ticket_order.buyer.get_full_name(),
                "order": ticket_order,
                "due_date": reservation_time(),
            }
            render_invoice = invoice_template.render(invoice_context, request=request)
            pdf_file = HTML(string=render_invoice).write_pdf()
            
            # Save PDF to order's receipt
            buffer = BytesIO(pdf_file)
            ticket_order.receipt.save(f'{ticket_order.order_number}_invoice.pdf', buffer)
            
            # Prepare files for email attachments
            files = [{"file_content": base64.b64encode(pdf_file).decode(), "filename": f'{ticket_order.order_number}_invoice.pdf'}]

            context = {
                "user": ticket_order.buyer.get_full_name(),
                "order": ticket_order,
            }

            if ticket_order.paid == PaymentStatus.PAID:
                mail_subject = f"Your tickets for {ticket_order.event.title} on {ticket_order.event.date_time_formatter()}"
                message_template = "emails/tickets/ticket-order-email.html"
                
                with open(ticket_order.tickets_pdf_file.path, 'rb') as pdf_file:
                    pdf_content = pdf_file.read()
                    encoded_content = base64.b64encode(pdf_content).decode()
                    files.append({"file_content": encoded_content, "filename": f'{ticket_order.order_number}_tickets.pdf'})
            else:
                mail_subject = f"Your tickets order for {ticket_order.event.title} on {ticket_order.event.date_time_formatter()} was cancelled"
                message_template = "emails/tickets/order-cancelled.html"

            # Render email content
            message = render_to_string(message_template, context, request=request)

            # Send email with attachments
            sent = send_html_email_with_attachments(ticket_order.email, mail_subject, message, "BBGI Events <events@bbgi.co.za>", files)
            sent = send_html_email_with_attachments('gumedethomas12@gmail.com', mail_subject, message, "BBGI Events <events@bbgi.co.za>", files)
            if not sent:
                email_logger.error(f"Failed to send tickets email to {ticket_order.email} for order number {ticket_order.order_number}")
                

            messages.info(request, "This order was verified and client was notified")
            return redirect("bbgi_home:all-ticket-orders")

        except Exception as ex:
            email_logger.error(f"Error in sending ticket email: {ex}")
            
            messages.info(request, "This order was verified and client was notified")
            return redirect("bbgi_home:all-ticket-orders")
    
    
    return render(request, "payments/tickets/verify-payment.html", {"ticketorder": ticket_order})

@login_required
def tickets_payment_cancelled(request, ticket_order_id):
    ticket_order = get_object_or_404(TicketOrderModel, id=ticket_order_id)
    ticket_order.delete()
    messages.success(request,"Payment cancelled successfully")
    return redirect("events:events")

@login_required
def tickets_payment_failed(request, ticket_order_id):
    ticket_order = get_object_or_404(TicketOrderModel, id=ticket_order_id)

    try:
        payment_information = PaymentInformation.objects.get(id = ticket_order.checkout_id)
        payment_information.order_number = ticket_order.order_number
        payment_information.save(update_fields=["order_number"])
        updated = update_payment_status_ticket_order(json.loads(payment_information.data), request, ticket_order)
        
        if updated:
            print("done")
        else:
            print("Not done")

    except PaymentInformation.DoesNotExist:
        pass

    return render(request, "payments/tickets/failed.html")

def resend_tickets(request, order_uuid):
    order = get_object_or_404(TicketOrderModel, id=order_uuid, buyer=request.user)
    if order.paid == PaymentStatus.NOT_PAID:
        messages.error(request, "You have not paid for your tickets, if you did pay for them, please contact us <b>support@ndwandwafam.co.za</b>")
        return redirect("events:manage-ticket-order", id=order_uuid)

    protocol = "https" if request.is_secure() else "http"
    domain = get_current_site(request).domain
    resend_tickets_2_task.delay(order.checkout_id, protocol, domain)
    messages.success(request, "Your tickets were successfully sent, if you don't receive them, please contact us <b>support@ndwandwafam.co.za</b>")
    return redirect("events:manage-ticket-order", order_id=order.id)

