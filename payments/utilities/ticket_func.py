import logging
from campaigns.utils import PaymentStatus
from events.models import TicketOrderModel
from payments.utilities.custom_email import send_tickets_email
from payments.utilities.wallet_update_func import update_payment_details, update_wallet

logger = logging.getLogger("payments")

def update_payment_status_ticket_order(data, request,  ticket_order: TicketOrderModel):
    try:
        if data["type"] == "payment.succeeded":
            payment_status = PaymentStatus.PAID
            admin_cost = ticket_order.calculate_total_admin_cost()
            organiser_profit = ticket_order.calculate_actual_profit()
            if ticket_order.event.organiser:
                wallet_updated = update_wallet(ticket_order.event.organiser, organiser_profit, admin_cost, ticket_order.order_number, ticket_order.id)
                if not wallet_updated:
                    logger.error("Failed to update wallet")
        else:
                payment_status = PaymentStatus.NOT_PAID
            
        update_payment_details(ticket_order, data, payment_status)
        sent = send_tickets_email(data["type"], ticket_order, request)

        if sent:
            return True
        else:
            return False
    except Exception as ex:
         logger.error(ex)
         return False
