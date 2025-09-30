from celery import shared_task
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from accounts.utilities.company import COMPANY
from accounts.utilities.custom_email import send_html_email
from listings.models import Business
import logging

logger = logging.getLogger("tasks")
email_logger = logging.getLogger("emails")

@shared_task
def send_on_boarding_email(listing_id):
    try:
        
        
            listing = Business.objects.get(id=listing_id)
            send_html_email('New Listing Added', 'listings@bbgi.co.za', 'emails/listing-confirmation.html', {"listing": listing})
            context = {
                    "protocol": "https",
                    "domain": "bbgi.co.za",
                    "listing": listing,
                    "facebook": COMPANY["facebook"],
                    "linkedin": COMPANY["linkedIn"],
                    "instagram": COMPANY["instagram"],
                    "youtube": COMPANY["youtube"], 
                    "tiktok": COMPANY["tiktok"],
                    
                }
        # message = render_to_string("emails/email_to_community.html", context,
        #     )
            html_content = render_to_string("emails/on-boarding-listing.html", context)
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
                subject=f"BBGI | Company Added Successfully",
                body=html_content,
                from_email="BBGI Business Admin",
                to=[listing.owner.email]
            )
            email.content_subtype = 'html'
            
            email2 = EmailMessage(
                subject=f"BBGI | Company Added Successfully",
                body=html_content,
                from_email="BBGI Business Admin",
                to=["gumedethomas12@gmail.com"]
            )
            email2.content_subtype = 'html'

            sent = email.send(fail_silently=False)
            sent2 = email2.send(fail_silently=False)
            if not sent or not sent2:
                logger.error(f"Email not sent to {listing.owner.email} from Admin")
                return f"Email not sent to {listing.owner.email} from Admin"
            return f"Email to {listing.owner.email} from Admin"
            
    except Exception as ex:
        logger.error(ex)
        return f"Email not to {listing.owner.email} from Admin"