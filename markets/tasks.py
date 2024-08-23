from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from accounts.utilities.company import COMPANY
from listings.models import Business
from markets.models import Service, Qoutation
import logging, base64

logger = logging.getLogger("tasks")
email_logger = logging.getLogger("emails")

 


def send_email_to_owner(domain, protocol, qoute_id):
    try:
        qoute = Qoutation.objects.filter(id=qoute_id).first()
        context = {
                    "protocol": protocol,
                    "domain": domain,
                    "owner": qoute.service.business.owner.get_full_name(),
                    "quote": qoute,
                    "facebook": COMPANY["facebook"],
                    "linkedin": COMPANY["linkedIn"],
                    "instagram": COMPANY["instagram"],
                    "youtube": COMPANY["youtube"], 
                    "tiktok": COMPANY["tiktok"],
                    
                }
        message = render_to_string("emails/quotation_request_email.html", context,
            )
        email = EmailMessage(
            subject="BBGI | Quote Request",
            body=message,
            from_email="BBGI Quotes <orders@bbgi.co.za>",
            to=[qoute.service.business.email, qoute.service.business.owner.email]
        )
        email.content_subtype = 'html'

        if qoute.file:
            
            email.attach_file(qoute.file.path)

        if not email.send():
            logger.error(f"Email not sent to {qoute.service.business.email} for qoute {qoute.id}")
        
    except Exception as ex:
        logger.error(ex)