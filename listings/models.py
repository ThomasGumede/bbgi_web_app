from django.db import models
from django.db.models import Avg, Count
from django.urls import reverse
from accounts.custom_models.abstracts import PHONE_VALIDATOR
from accounts.custom_models.choices import StatusChoices
from accounts.models import AbstractCreate
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.utils.translation import gettext as _
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.utilities.validators import validate_fcbk_link, validate_in_link, validate_insta_link, validate_twitter_link
from listings.utilities.file_handlers import handle_business_file_upload, handle_business_verification_file_upload

DAYCHOICES = [
    ("MO", "Monday"),
    ("TU", "Tuesday"),
    ("WE", "Wednesday"),
    ("TH", "Thursday"),
    ("FR", "Friday"),
    ("SA", "Saturday"),
    ("SU", "Sunday")
    ]

BBBEE_RATINGS = [
    ("BEL1", "BEE Level 1"),
    ("BEL2", "BEE Level 2"),
    ("BEL3", "BEE Level 3"),
    ("BEL4", "BEE Level 4"),
    ("BEL5", "BEE Level 5"),
    ("BEL6", "BEE Level 6"),
    ("BEL7", "BEE Level 7"),
    ("NOT", "Not sure"),
    ("NC", "Non-compliance")
    ]

PROVINCES = [
    ("kzn", "KwaZulu-Natal"),
    ("mp", "Mpumalanga"),
    ("nw", "North-West"),
    ("fs", "Free-State"),
    ("wc", "Western Cape"),
    ("lp", "Limpopo"),
    ("gp", "Gauteng"),
    ("ec", "Eastern Cape"),
    ("nc", "Northern Cape"),
]

class OperatingChoices(models.TextChoices):
    CUSTOM = ("CUSTOM", "Custom")
    CLOSED = ("CLOSED", "Closed")
    OPEN = ("OPEN", "Open 24/7")

class Category(AbstractCreate):
    thumbnail = models.ImageField(upload_to="category/business/", null=True, blank=True)
    slug = models.SlugField(max_length=350, unique=True, db_index=True)
    label = models.CharField(max_length=250, unique=True)
    

    def __str__(self):
        return str(self.label)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.label)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

class Business(AbstractCreate):
    background_image = models.ImageField(help_text=_("Upload company/business background image."), upload_to=handle_business_file_upload, blank=True, null=True)
    logo = models.ImageField(help_text=_("Upload company/business logo."), upload_to=handle_business_file_upload, blank=True, null=True)
    title = models.CharField(help_text=_("Enter title for your company/business"), max_length=150, unique=True)
    slogan = models.CharField(_("Enter your business slug"), max_length=350, null=True, blank=True)
    slug = models.SlugField(max_length=250, blank=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None, related_name="businesses")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="businesses")
    details = models.TextField(help_text=_("Enter additional details about your company/business"), null=True, blank=True)
    main_address = models.CharField(max_length=300, help_text=_("Enter main office address seperated by comma"), null=True, blank=True)
    map_coordinates  = models.CharField(max_length=300, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    email = models.EmailField(_("Enter your business email"), max_length=250, blank=True, null=True)
    bbbee_level = models.CharField(max_length=100, choices=BBBEE_RATINGS)
    province = models.CharField(max_length=300, choices=PROVINCES)
    phone = models.CharField(help_text=_("Enter your business number"), max_length=15, validators=[PHONE_VALIDATOR], null=True, blank=True)
    alternative_phone = models.CharField(help_text=_("Enter your business number"), max_length=15, validators=[PHONE_VALIDATOR], null=True, blank=True)
    facebook = models.URLField(validators=[validate_fcbk_link], blank=True, null=True)
    twitter = models.URLField(validators=[validate_twitter_link], blank=True, null=True)
    instagram = models.URLField(validators=[validate_insta_link], blank=True, null=True)
    linkedIn = models.URLField(validators=[validate_in_link], blank=True, null=True)
    status = models.CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.NOT_APPROVED)
    is_completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Business'
        verbose_name_plural = 'Businesses'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Business, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse("listings:get-listing", kwargs={"listing_slug": self.slug})
    
    def get_full_location(self):
        return self.main_address

    def get_average_rating(self):
        reviews = self.reviews.all()
        average_rating = reviews.aggregate(Avg('rating_value'))['rating_value__avg'] or 0
        text = round(average_rating, 1)
        
        return text
    
    def get_avg_rating(self):
        return self.reviews.aggregate(avg_rating_value=Avg('rating_value'))['avg_rating_value']
        
    
    def get_location(self):
        return self.main_address

    def is_open(self):
            now = timezone.now()
            current_day = now.strftime('%a').upper()[:2]
            current_time = now.time()

            business_hours_today = self.business_hours.filter(day=current_day)
            for hours in business_hours_today:
                if hours.operating:
                    if hours.open_time <= current_time <= hours.close_time:
                        return True
                    else:
                        return False
                else:
                    return False

    
class BusinessContent(AbstractCreate):
    image = models.ImageField(help_text=_("Upload company/business images."), upload_to=handle_business_file_upload, blank=True, null=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="images")

class BusinessReview(AbstractCreate):
    rating_value = models.IntegerField(validators=[
            MinValueValidator(1),   
            MaxValueValidator(5)  
        ])
    commenter = models.ForeignKey(get_user_model(), related_name="reviews", on_delete=models.SET_NULL, null=True)
    commenter_email = models.EmailField()
    commenter_full_names = models.CharField(max_length=250)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="reviews")
    comment_title = models.CharField(max_length=250)
    comment = models.TextField()

    class Meta:
        verbose_name = 'Business Review'
        verbose_name_plural = 'Business Reviews'

    def __str__(self) -> str:
        return self.commenter_email

class BusinessHour(AbstractCreate):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="business_hours")
    day = models.CharField(max_length=250, choices=DAYCHOICES, default=DAYCHOICES[1])
    operating = models.BooleanField(default=True)
    open_time = models.TimeField()
    close_time = models.TimeField()

    class Meta:
        unique_together = ('business', 'day')
        verbose_name = 'Business Hour'
        verbose_name_plural = 'Business Hours'

    def get_open_time(self):
        return self.open_time

    def get_close_time(self):
        return self.close_time

    def get_operating_hours(self):
        return f"{self.open_time} - {self.close_time}"

class BusinessLocation(AbstractCreate):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="business_locations", null=True)
    location_title = models.CharField(max_length=350, help_text=_("Enter your business branch name"), blank=True, null=True)
    email = models.EmailField(help_text=_("Enter your business branch email"), max_length=250, blank=True, null=True)
    phone = models.CharField(help_text=_("Enter your business branch number"), max_length=15, validators=[PHONE_VALIDATOR], unique=True, null=True, blank=True)
    address = models.CharField(max_length=400, help_text=_("Enter office address seperated by comma"))
    map_coordinates  = models.CharField(max_length=300, blank=True, null=True)
    address_id = models.CharField(max_length=300, null=True, blank=True)
    
    def __str__(self):
        return self.address
    


@receiver(pre_delete, sender=Business)
def delete_business_images_hook(sender, instance, using, **kwargs):
    if instance.background_image:
        instance.background_image.delete()
    if instance.logo:
        instance.logo.delete()

@receiver(pre_delete, sender=BusinessContent)
def delete_business_content_images_hook(sender, instance, using, **kwargs):
    if instance.image:
        instance.image.delete()