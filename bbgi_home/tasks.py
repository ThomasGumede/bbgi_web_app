from celery import shared_task
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from accounts.utilities.company import COMPANY
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger("tasks")
email_logger = logging.getLogger("emails")

 
@shared_task
def send_admin_email_to_bbgi_community(message, topic):
    try:
        
        recipients = get_user_model().objects.all().exclude(email='')
        
        for recipient in recipients:
            context = {
                    "protocol": "https",
                    "domain": "bbgi.co.za",
                    "topic": topic,
                    "message": message,
                    "name": f"{recipient.title} {recipient.get_full_name()}",
                    "facebook": COMPANY["facebook"],
                    "linkedin": COMPANY["linkedIn"],
                    "instagram": COMPANY["instagram"],
                    "youtube": COMPANY["youtube"], 
                    "tiktok": COMPANY["tiktok"],
                    
                }
        # message = render_to_string("emails/email_to_community.html", context,
        #     )
            html_content = render_to_string("emails/email_to_community.html", context)
            # Create email message
            # email = EmailMultiAlternatives(
            #     subject=f"BBGI | {topic}",
            #     body="This is an HTML email. If you're seeing this, your email client does not support HTML.",
            #     from_email="BBGI Admin <admin@bbgi.co.za>",
            #     to=['gumedethomas12@gmail.com'],
            # )
            # email.attach_alternative(html_content, "text/html")
            # sent = email.send(fail_silently=False)
        
            email = EmailMessage(
                subject=f"BBGI | {topic}",
                body=html_content,
                from_email="BBGI Admin <admin@bbgi.co.za>",
                to=[recipient.email]
            )
            email.content_subtype = 'html'

            sent = email.send(fail_silently=False)
            if not sent:
                logger.error(f"Email not sent to {recipient.email} from Admin")
                return f"Email not sent to {recipient.email} from Admin"
            return f"Email not to {recipient.email} from Admin"
            
    except Exception as ex:
        logger.error(ex)

def send_email_to_admin(subject, message, from_email, name):
    try:
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=["gumedethomas12@gmail.com", "info@bbgi.co.za", "sazi.ndwandwa@gmail.com"]
        )
        if not email.send():
            return f"Email not sent from {from_email}"
        else:
            return "Email sent"
    except Exception as ex:
        logger.error(ex)
