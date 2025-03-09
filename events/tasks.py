from celery import shared_task
import logging
from accounts.custom_models.choices import StatusChoices
from events.models import TicketOrderModel, EventModel
from campaigns.tasks import update_status_email
from django.utils import timezone
from campaigns.utils import PaymentStatus
import random, barcode, logging, qrcode, uuid
from events.models import TicketModel, TicketOrderModel, EventModel
from barcode.writer import ImageWriter

from events.utils import create_new_barcode_number

logger = logging.getLogger("utils")
email_logger = logging.getLogger("emails")

def handle_event_file_upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    return f"event/{filename}"


    
logger = logging.getLogger("tasks")

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
        for ticket in TicketModel.objects.filter(ticket_order=order):
            ticket_url = f'https://bbgi.co.za/ticket-types/verify/{order.order_number}/{ticket.id}'
            barcode_value = create_new_barcode_number()
            barcode_image = barcode.Code128(barcode_value, writer=ImageWriter())
            barcode_image.save(f'media/tickets/barcodes/' + order.order_number)
                    
            qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4,
                    )
            
            qr.add_data(ticket_url)
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")
            qr_image.save(f'media/tickets/qrcodes/' + order.order_number + '_qrcode.png')
            
            ticket.qrcode_url = ticket_url
            ticket.barcode_value = barcode_value
            ticket.qrcode_image = f'tickets/qrcodes/' + order.order_number + '_qrcode.png'
            ticket.barcode_image = f'tickets/barcodes/' + order.order_number + '.png'
            ticket.save(update_fields=["qrcode_url", "barcode_value", "qrcode_image", "barcode_image"])
        
        return "Successfully created tickets"

    except TicketOrderModel.DoesNotExist as ex:
        logger.error(ex)
        return "Didn't create a ticket"
    
    except Exception as ex:
        logger.error(ex)
        return "Didn't create a ticket"
