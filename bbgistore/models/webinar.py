from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import AbstractCreate
from django.contrib.auth import get_user_model
from bbgistore.models.abstract import StoreCategory, StoreItem, Person
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError

from bbgistore.utilities.validators import generate_unique_slug, validate_video_file_type

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
    presenters = models.ManyToManyField(Person, related_name="webinars", blank=True, help_text=_("Select presenters for this webinar"))
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
    added_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name="webinars", help_text=_("The person who added this webinar."))
    
    
    class Meta:
        verbose_name = "Webinar"
        verbose_name_plural = "Webinars"
        ordering = ["-created"]
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.title)
        super().save(*args, **kwargs)
        
    def clean(self):
        if self.webinar_type == self.Type.LIVE:

            if not self.start_time:
                raise ValidationError("Start time is required.")

            if not self.end_time:
                raise ValidationError("End time is required.")

            if not self.registration_deadline:
                raise ValidationError("Registration deadline is required.")

            if not self.max_participants:
                raise ValidationError("Maximum participants is required.")

        if self.webinar_type == self.Type.RECORDED:

            self.start_time = None
            self.end_time = None
            self.registration_deadline = None
            self.max_participants = None
        
        super().clean()
            
    @property
    def total_videos(self):
        return self.videos.count()
    
    @property
    def total_duration(self):
        from datetime import timedelta

        total = timedelta()

        for video in self.videos.all():
            if video.duration:
                total += video.duration

        return total
    
    @property
    def enrollment_count(self):
        return self.enrollments.count()


    @property
    def attendee_count(self):
        return self.enrollments.filter(
            status=WebinarEnrollment.Status.ATTENDED
        ).count()


    @property
    def completed_count(self):
        return self.enrollments.filter(
            status=WebinarEnrollment.Status.COMPLETED
        ).count()


    @property
    def available_seats(self):
        if self.max_participants is None:
            return None

        return max(
            self.max_participants - self.enrollment_count,
            0,
        )


    @property
    def is_full(self):
        if self.max_participants is None:
            return False

        return self.enrollment_count >= self.max_participants

    def __str__(self):
        return self.title
    
    @property
    def presenters_list(self):
        return ", ".join([presenter.full_names for presenter in self.presenters.all()])
    
class WebinarVideo(AbstractCreate):
    webinar = models.ForeignKey(
        Webinar,
        on_delete=models.CASCADE,
        related_name="videos"
    )

    title = models.CharField(max_length=255, help_text="Enter title for this webinar video")

    description = models.TextField(blank=True, help_text="Enter description for this webinar video")

    order = models.PositiveIntegerField(default=1, help_text="Enter the order of this video in the webinar sequence")

    duration = models.DurationField(
        null=True,
        blank=True, help_text="Enter the duration of this video in HH:MM:SS format"
    )

    thumbnail = models.ImageField(
        upload_to="bbgistore/webinar_thumbnails/",
        blank=True,
        null=True, help_text="Choose a thumbnail image for this webinar video"
    )

    video = models.FileField(
        upload_to="bbgistore/webinars/",
        validators=[validate_video_file_type], help_text="Upload the video file for this webinar video", blank=True, null=True
    )
    video_link = models.URLField(help_text=_("Enter video external url if available"), blank=True, null=True)
    
    is_preview = models.BooleanField(
        default=False,
         help_text="Indicate whether this video is a free preview before purchase."
    )

    is_bonus = models.BooleanField(
        default=False, help_text="Indicate whether this video is a bonus video included with the webinar."
    )

    is_active = models.BooleanField(
        default=True
    )
    
    def clean(self):
        from urllib.parse import urlparse
        super().clean()
        if self.video == None and self.video_link == None:
            raise ValidationError("Please provide atleast one video source, either video link or video file")
        
        if self.video_link:
            parse = urlparse(self.video_link)
            if not parse.scheme:
                self.video_link = f"https://{self.video_link}"

    class Meta:
        ordering = ["order", "created"]
        
class WebinarEnrollment(AbstractCreate):
    class Status(models.TextChoices):
        REGISTERED = "registered", _("Registered")
        ATTENDED = "attended", _("Attended")
        COMPLETED = "completed", _("Completed")
        CANCELLED = "cancelled", _("Cancelled")
        NO_SHOW = "no_show", _("No Show")

    webinar = models.ForeignKey(
        Webinar,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="webinar_enrollments",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.REGISTERED,
    )

    registered_at = models.DateTimeField(
        auto_now_add=True,
    )

    attended_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    progress = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
        ],
        help_text=_("Completion percentage (0-100)."),
    )

    certificate_issued = models.BooleanField(
        default=False,
    )

    certificate_issued_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    certificate_number = models.CharField(
        max_length=100,
        blank=True,
    )

    cpd_points_awarded = models.PositiveIntegerField(
        default=0,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["-registered_at"]

        verbose_name = _("Webinar Enrollment")
        verbose_name_plural = _("Webinar Enrollments")

        constraints = [
            models.UniqueConstraint(
                fields=["webinar", "user"],
                name="unique_webinar_enrollment",
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.webinar}"   
        
