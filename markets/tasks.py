from celery import shared_task
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from accounts.utilities.company import COMPANY
from listings.models import Business
from markets.models import Qoutation, Service, RequestService
import logging, base64
from django.contrib.auth import get_user_model

logger = logging.getLogger("tasks")
email_logger = logging.getLogger("emails")

@shared_task
def send_email_to_bbgi_community(domain, protocol, qoute_id):
    try:
        qoute = RequestService.objects.get(id=qoute_id)
        recipients = get_user_model().objects.values_list('email', flat=True).exclude(email='')
        context = {
                    "protocol": protocol,
                    "domain": domain,
                    
                    "quote": qoute,
                    "facebook": COMPANY["facebook"],
                    "linkedin": COMPANY["linkedIn"],
                    "instagram": COMPANY["instagram"],
                    "youtube": COMPANY["youtube"], 
                    "tiktok": COMPANY["tiktok"],
                    
                }
        # message = render_to_string("emails/quotation_request_email.html", context,
        #     )
        html_content = render_to_string("emails/quotation_request_email.html", context)
        for recipient in recipients:
        
            email = EmailMessage(
                subject=f"Quote Request for Service - {qoute.service_title}",
                body=html_content,
                from_email="BBGI Quotes <orders@bbgi.co.za>",
                to=['gumedethomas12@gmail.com']
            )
            email.content_subtype = 'html'

            if qoute.file:
                email.attach_file(qoute.file.path)
                
            sent = email.send(fail_silently=False)
            if not sent:
                logger.error(f"Email not sent to {qoute.service.business.email} for qoute {qoute.id}")
            
    except RequestService.DoesNotExist as ex:
        logger.error(ex)
    except Exception as ex:
        logger.error(ex)

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