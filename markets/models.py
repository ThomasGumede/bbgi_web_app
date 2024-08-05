from django.db import models
from django.urls import reverse
from accounts.custom_models.abstracts import PHONE_VALIDATOR, AbstractCreate
from django.core.validators import MinValueValidator
from django.utils.translation import gettext as _
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify

from listings.models import Business
from markets.utilities.file_handlers import handle_service_file_upload

class Service(AbstractCreate):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="services")
    image = models.ImageField(upload_to=handle_service_file_upload, blank=True, null=True)
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=250)
    description = models.TextField()
    price_decription = models.CharField(help_text=_("Enter service price decription e.g Callout fee"), max_length=150, null=True, blank=True, default="")
    price = models.DecimalField(help_text=_("Enter service price e.g 300.00"), max_digits=1000, decimal_places=2, null=True, blank=True)
    on_discount = models.BooleanField(default=False)
    discount_percentage = models.DecimalField(max_digits=1000, decimal_places=2, help_text=_("Enter discount percentage, e.g 100"), null=True, blank=True)
    discount_description = models.CharField(max_length=150, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Service, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        ordering = ["-created"]

    def __str__(self):
        return self.title

TIME_CHOICES = (
    ("I'm flexible", "I'm flexible"),
    ("As soon as possible", "As soon as possible"),
    ("It an emergency", "It an emergency"),
    ("Approved Payout", "Approved Payout"),
    ("I have a specific date in mind", "I have a specific date in mind"),
    
)

CALL_CHOICES = (
    ("Morning(7am - 12pm)", "Morning(7am - 12pm)"),
    ("Afternoon (12pm - 5pm)", "Afternoon (12pm - 5pm)"),
    ("Late (5pm - till late)", "Late (5pm - till late)"),
    ("Anytime", "Anytime"),
    
)

class Qoutation(AbstractCreate):
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="qoutations")
    client = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="qoutations")
    file = models.ImageField(upload_to="business/qoutation/", null=True, blank=True)
    full_names = models.CharField(max_length=350)
    phone = models.CharField(help_text=_("Enter your cellphone number"), max_length=15, validators=[PHONE_VALIDATOR])
    email = models.EmailField(help_text=_("Enter your email address"), max_length=254)
    description = models.TextField(null=True, blank=True)
    is_location_based = models.BooleanField(help_text=_("Does this job need to be done on a specific location?"), default=False)
    location = models.CharField(help_text=_("Enter your location, e.g 123 St, KZN, 3915"), max_length=350, blank=True, null=True)
    call_at = models.CharField(help_text=_("When should we contact you?"), choices=CALL_CHOICES, max_length=150)
    time = models.CharField(max_length=150, choices=TIME_CHOICES, help_text=_("When do you need the service to be completed?"))
    date = models.DateField(null=True, blank=True, validators=[MinValueValidator(timezone.now(), "Date should not be less that today's date")])


    def __str__(self):
        return self.full_names + self.call_at
    
    class Meta:
        verbose_name = _("Qoutation Request")
        verbose_name_plural = _("Qoutation Requests")
        ordering = ["-created"]
