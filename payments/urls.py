from django.urls import path
from payments.views.contribution import contributions_payment_cancelled, contributions_payment_success, contribution_payment, contributions_payment_failed
from payments.views.subscribe import subscription_payment, subscription_payment_cancelled, subscription_payment_failed, subscription_payment_success
from payments.views.ticket_order import tickets_payment_cancelled, tickets_payment_failed, verify_ticket_payment_order, tickets_payment_success, payment, resend_tickets
from payments.views.webhook import create_webhook, get_webhooks, webhook, delete_webhook

app_name = "payments"
urlpatterns = [
    
    path("payments/webhook", webhook, name="webhook"),
    path("webhook/create", create_webhook, name="create_webhook"),
    path("get/webhooks", get_webhooks, name="get_webhook"),
    path("delete/webhook/<webhook_id>", delete_webhook, name="delete_webhook"),
    path("contributions/payment/<contribution_id>", contribution_payment, name="contribution-payment"),
    path("contributions/payment/cancelled/<contribution_id>", contributions_payment_cancelled, name="contribution-payment-cancelled"),
    path("contributions/payment/failed/<contribution_id>", contributions_payment_failed, name="contribution-payment-failed"),
    path("contributions/payment/success/<contribution_id>", contributions_payment_success, name="contribution-payment-success"),

    path("subscriptions/payment/<subscription_id>", subscription_payment, name="subscription-payment"),
    path("subscriptions/payment/cancelled/<subscription_id>", subscription_payment_cancelled, name="subscription-payment-cancelled"),
    path("subscriptions/payment/failed/<subscription_id>", subscription_payment_failed, name="subscription-payment-failed"),
    path("subscriptions/payment/success/<subscription_id>", subscription_payment_success, name="subscription-payment-success"),

    path("tickets/payment/<uuid:ticket_order_id>", payment, name="ticket-payment"),
    path("tickets/payment/cancelled/<uuid:ticket_order_id>", tickets_payment_cancelled, name="ticket-payment-cancelled"),
    path("tickets/payment/failed/<uuid:ticket_order_id>", tickets_payment_failed, name="ticket-payment-failed"),
    path("tickets/payment/success/<uuid:ticket_order_id>", tickets_payment_success, name="ticket-payment-success"),
    path("tickets/payment/verify/<uuid:ticket_order_id>", verify_ticket_payment_order, name="verify-ticket-payment"),
    path("tickets/manage/resend/<uuid:order_uuid>", resend_tickets, name="resend-tickets")
    
]
