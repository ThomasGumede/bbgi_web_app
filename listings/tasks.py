from celery import shared_task
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from accounts.utilities.company import COMPANY
from accounts.utilities.custom_email import send_html_email
from django.db.models import Avg
from django.utils import timezone
from listings.models import Business, BusinessAnalytics
import logging

logger = logging.getLogger("tasks")
email_logger = logging.getLogger("emails")

@shared_task
def update_business_analytics(business_id):
    try:
        business = Business.objects.get(id=business_id)
        analytics, created = BusinessAnalytics.objects.get_or_create(business=business, date=timezone.now().date())
        
        if created:
            return f"Analytics updated for {business.title}"
        
        analytics.total_views += 1
        analytics.total_bookings = 0
        analytics.total_messages = business.messages.count()
        analytics.average_rating = business.reviews.aggregate(Avg('rating_value'))['rating_value__avg'] or 0
        analytics.save()
        return f"Analytics updated for {business.title}"
    except Business.DoesNotExist:
        logger.error(f"Business with id {business_id} does not exist")
        return f"Business with id {business_id} does not exist"
    except Exception as ex:
        logger.error(ex)
        return f"Analytics not updated for business with id {business_id}"

# @shared_task
# def send_notification_email_to_owner(message_id, protocol = 'https', domain = 'bbgi.co.za'):
#     try:
        
#         message = BusinessMessages.objects.get(id=message_id)
#         context = {
            
#             "message": message,
#             "protocol": protocol,
#             "domain": domain,
#         }
#         mail_subject = f"{message.sender_full_names} sent you a message regarding {message.business.title}"
#         message_template = "emails/manage-event-email.html"
        
#         # Render email content
#         message = render_to_string(message_template, context)

#         # Send email with attachments
#         email = EmailMessage(
#             subject=mail_subject,
#             body=message,
#             from_email="BBGI Listings <listings@bbgi.co.za>",
#             to=[message.business.owner.email],
#         )
#         email.send(fail_silently=False)
#         return f"Email sent to {message.business.owner.email} from Admin"
    
#     except BusinessMessages.DoesNotExist:
#         logger.error(f"Message with id {message_id} does not exist")
#         return f"Message with id {message_id} does not exist"
    
#     except Exception as ex:
#         logger.error(ex)
#         return f"Email not sent to {message.business.owner.email} from Admin"

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
                from_email="BBGI Business Admin <noreply@bbgi.co.za>",
                to=[listing.owner.email]
            )
            email.content_subtype = 'html'
            
            email2 = EmailMessage(
                subject=f"BBGI | Company Added Successfully",
                body=html_content,
                from_email="BBGI Business Admin <noreply@bbgi.co.za>",
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
