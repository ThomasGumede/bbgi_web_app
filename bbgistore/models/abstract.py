from django.db import models
from accounts.models import AbstractCreate
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from taggit_autosuggest.managers import TaggableManager
from tinymce.models import HTMLField

from bbgistore.utilities.validators import validate_recap_video_file_size, validate_video_file_type

class StoreStatusChoices(models.TextChoices):
    DRAFT = "draft", _("Draft")
    PUBLISHED = "published", _("Published")

class StoreItem(AbstractCreate):
    from bbgi_home.models import UUIDTaggedItem
    title = models.CharField(max_length=255, help_text=_("Enter Title for this book/webinar/course"))
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=300, help_text=_("Enter short description about this book/webinar/course"))
    description = HTMLField(help_text=_("Enter full description about this book/webinar/course"))
    thumbnail = models.ImageField(upload_to="bbgistore/thumbnails/", help_text=_("Choose an image for this book/webinar/course"), null=True, blank=True)
    recap_video = models.FileField(upload_to="bbgistore/videos/", help_text=_("Provide a short video explaination for this book/webinar/course, should be not longer than 5 minutes"), validators=[validate_video_file_type, validate_recap_video_file_size], null=True, blank=True)
    recap_video_url = models.URLField(help_text=_("Provide recap video url for this book/webinar/course"), blank=True, null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    is_free = models.BooleanField(default=False)
    status = models.CharField(max_length=30, choices=StoreStatusChoices.choices, default=StoreStatusChoices.DRAFT)
    featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    tags = TaggableManager(
        through=UUIDTaggedItem,
        help_text=_("Add tags separated by commas"), blank=True
    )

    class Meta: 
        verbose_name = "Store Item"
        verbose_name_plural = "Store Items"
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["slug"]),
        ]
        abstract=True

class StoreCategory(AbstractCreate):
    title = models.CharField(max_length=250)
    slug=models.SlugField(unique=True)
    icon = models.CharField(max_length=250, help_text="Enter category icon e.g <i fa-solid fa-book></i>", blank=True, null=True)

    class Meta:
        ordering = ("-created",)
        verbose_name_plural = "Store Categories"
        
    @property
    def book_count(self):
        return self.books.count()

    def __str__(self):
        return self.title
    
class Person(AbstractCreate):
    full_names = models.CharField(max_length=250, help_text=_("Enter full names of the Author/Contributor/Instructor"))
    thumbnail = models.ImageField(upload_to="bbgistore/thumbnails/", help_text=_("Choose an image for this Author/Contributor/Instructor"), null=True, blank=True)
    biography = models.TextField(blank=True, help_text=_("Enter biography"))
    bbgi_account = models.OneToOneField(get_user_model(), related_name="author_or_instructor", on_delete=models.SET_NULL, null=True, blank=True, help_text=_("If this person has bbgi account, please select them or leave the space blank"), verbose_name=_("BBGI Account"))

    class Meta:
        ordering = ("-created",)
        verbose_name = "Author/Contributor/Instructor"
        verbose_name_plural = "Authors, Contributors and Instructors"

    def __str__(self):
        return self.full_names
    
    
    
    
