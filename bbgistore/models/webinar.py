from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import AbstractCreate
from django.contrib.auth import get_user_model
from bbgistore.models.abstract import StoreCategory, StoreItem, Person
from django.utils.translation import gettext as _
from django.template.defaultfilters import slugify

from bbgistore.utilities.validators import validate_video_file_type

class Webinar(StoreItem):
    class Type(models.TextChoices):
        LIVE = "live", _("Live")
        RECORDED = "recorded", _("Recorded")
        
    class Level(models.TextChoices):
        BEGINNER = "beginner", _("Beginner")
        INTERMEDIATE = "intermediate", _("Intermediate")
        ADVANCED = "advanced", _("Advanced")
        ALL = "all", _("All Levels")
        
    category = models.ForeignKey(StoreCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="webinars", help_text=_("Select category for this webinar"))
    presenters = models.ManyToManyField(Person, related_name="webinars", blank=True)
    start_time = models.DateTimeField(help_text=_("Enter the start date and time for the webinar, required for live webinars"), null=True, blank=True)
    end_time = models.DateTimeField(help_text=_("Enter the end date and time for the webinar, required for live webinars"), null=True, blank=True)
    duration = models.DurationField(help_text=_("Enter the total duration of the webinar in HH:MM:SS format"))
    max_participants = models.PositiveIntegerField(validators=[MinValueValidator(1, _("Maximum participants should be more than 0"))], help_text=_("Enter the maximum number of participants allowed for this webinar. required for live webinars"), null=True, blank=True)
    registration_deadline = models.DateTimeField(help_text=_("Enter the registration deadline for the webinar, required for live webinars"), null=True, blank=True)
    replay_available = models.BooleanField(default=False, help_text=_("Indicate whether a replay of the webinar will be available after the live session."))
    certificate_available = models.BooleanField(default=False, help_text=_("Indicate whether participants will receive a certificate of completion for this webinar."))
    cpd_points = models.PositiveIntegerField(validators=[MinValueValidator(0, _("CPD points should be 0 or more"))], help_text=_("Enter the number of CPD points awarded for attending this webinar. Set to 0 if not applicable."), default=0)
    webinar_type = models.CharField(max_length=20, choices=Type.choices, default=Type.LIVE)
    level = models.CharField(max_length=20, choices=Level.choices, default=Level.ALL)
    
    
    class Meta:
        verbose_name = "Webinar"
        verbose_name_plural = "Webinars"
        ordering = ["-created"]
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    @property
    def presenters_list(self):
        return ", ".join([presenter.full_names for presenter in self.presenters.all()])
    
class WebinarVideo(AbstractCreate):
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE, related_name="webinarvideos")
    video = models.FileField(upload_to="bbgistore/webinars/", validators=[validate_video_file_type])
    is_bonus = models.BooleanField(default=False, help_text=_("Indicate whether this video is a bonus video for the webinar."))
    
    class Meta:
        verbose_name = "Webinar Video"
        verbose_name_plural = "Webinar Videos"
        ordering = ["-created"]
    
    def __str__(self):
        return f"{self.webinar.title} video"