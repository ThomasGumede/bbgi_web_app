from celery import shared_task
import logging, json, base64
from io import BytesIO
from accounts.custom_models.choices import StatusChoices
from accounts.utilities.custom_email import send_html_email_with_attachments
from events.models import TicketOrderModel, EventModel, reservation_time
from campaigns.tasks import update_status_email
from django.utils import timezone
from campaigns.utils import PaymentStatus
import random, barcode, logging, qrcode, uuid
from events.models import TicketModel, TicketOrderModel, EventModel
from barcode.writer import ImageWriter
from django.template.loader import render_to_string
from django.template.loader import get_template
from weasyprint import HTML

from events.utils import create_new_barcode_number

logger = logging.getLogger("utils")
email_logger = logging.getLogger("emails")

def handle_event_file_upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    return f"event/{filename}"


    
logger = logging.getLogger("tasks")

@shared_task
def send_tickets_to_attendees(order_id, protocol = 'https', domain = 'bbgi.co.za'):
    try:
        invoice = get_template("emails/invoice.html")
        render_invoice = invoice.render({
                "buyer_full_name": order.buyer.get_full_name(),
                "order": order,
                "protocol": protocol,
                "domain": domain,
                "due_date": reservation_time(),
                
            })
        pdf_file = HTML(string=render_invoice).write_pdf()
        files = [
            (base64.b64encode(pdf_file).decode(), f'{order.order_number}_invoice.pdf')
        ]
        order = TicketOrderModel.objects.get(id=order_id)
        context = {
                    "protocol": protocol,
                    "domain": domain,
                    "user": order.buyer.get_full_name(),
                    "order": order,
                    
                }
        mail_subject = f"Your tickets for {order.event.title} on {order.event.date_time_formatter()}"
        message = render_to_string("emails/tickets/ticket-order-email.html", context,
            )
                    
        with open(order.tickets_pdf_file.path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()

        encoded_content = base64.b64encode(pdf_content).decode()
                
        files.append((encoded_content, f'{order.order_number}_tickets.pdf'))
        sent = send_html_email_with_attachments(order.email, mail_subject, message, "BBGI Events <events@bbgi.co.za>", files)
            
        if not sent:
            email_logger.error(f"Trouble sending tickets email to {order.email} order number {order.order_number}")

            return "Failed to send tickets to attendees"
            
        return "Successfully sent tickets to attendees"
        

    except TicketOrderModel.DoesNotExist:
        logger.error(f"Order with id {order_id} does not exist")
        return "Order does not exist"
    
    except Exception as ex:
        logger.error(f"Error sending tickets to attendees for order id {order_id}: {ex}")
        return "Failed to send tickets to attendees"

@shared_task
def check_ticket_2_order_payment(order_id):
    try:
        order = TicketOrderModel.objects.get(id=order_id)
        if order.paid == PaymentStatus.NOT_PAID:
            order.delete()
        
            return f"{order_id} was deleted"
    
    except TicketOrderModel.DoesNotExist:
        pass


@shared_task
def check_2_events_status():
    now = timezone.now()
    events = EventModel.objects.filter(event_enddate__lte=now)

    for event in events:
        if event.status != StatusChoices.COMPLETED:
            event.status = StatusChoices.COMPLETED
            event.save(update_fields=["status"])
            if not update_status_email("Event", event):
                logger.error("Failed to send email of Event status change")

    f"{events.count()} events were marked at completed"

@shared_task
def notify_2_organiser_event_of_status_change(event_id, domain = 'bbgi.co.za', protocol = 'https'):
    try:
        
        event = EventModel.objects.select_related("organiser").get(id=event_id)
        if not update_status_email("Event", event, domain, protocol):
            logger.error(f"Failed to send event status update - id {event.id}")

        return "Done"
    
    except EventModel.DoesNotExist:
        pass
    
@shared_task
def generate_qr_and_bacode_task(order_id):
    try:
        order = TicketOrderModel.objects.get(id=order_id)
        tickets = TicketModel.objects.filter(ticket_order=order)
        for ticket in tickets:
            ticket_url = f'https://bbgi.co.za/ticket-types/verify/{order.order_number}/{ticket.id}'
            barcode_value = create_new_barcode_number()
            barcode_image = barcode.Code128(barcode_value, writer=ImageWriter())
            barcode_image.save(f'media/tickets/barcodes/' + order.order_number + '_' + str(ticket.id))
                    
            qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4,
                    )
            
            qr.add_data(ticket_url)
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")
            qr_image.save(f'media/tickets/qrcodes/' + order.order_number + '_' + str(ticket.id) + '_qrcode.png')
            
            ticket.qrcode_url = ticket_url
            ticket.barcode_value = barcode_value
            ticket.qrcode_image = f'tickets/qrcodes/' + order.order_number + '_' + str(ticket.id) + '_qrcode.png'
            ticket.barcode_image = f'tickets/barcodes/' + order.order_number + '_' + str(ticket.id) + '.png'
            ticket.save(update_fields=["qrcode_url", "barcode_value", "qrcode_image", "barcode_image"])
            
        try:
                
            template = get_template("ticket/tickets.html")
            context = {"tickets": tickets, 
                            "event": order.event, 
                            "buyer_full_name": order.buyer.get_full_name(),
                            "order_number": order.order_number,
                            "created": order.created,
                            "domain": 'bbgi.co.za', 
                            "protocol": 'https'}
                
            render_template = template.render(context)
            pdf_file = HTML(string=render_template).write_pdf()
                    
            buffer = BytesIO(pdf_file)

            order.tickets_pdf_file.save(f'{order.order_number}_tickets.pdf', buffer)
            return "Successfully created tickets"
        except Exception as ex:
            logger.error(ex)
            return "Failed to create tickets"
            
        

    except TicketOrderModel.DoesNotExist as ex:
        logger.error(ex)
        return "Didn't create a ticket"
    
    except Exception as ex:
        logger.error(ex)
        return "Didn't create a ticket"
