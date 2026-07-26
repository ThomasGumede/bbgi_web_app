from bbgistore.tasks import process_video
from django.db import transaction
from django.db.models.signals import post_save
from bbgistore.models.webinar import WebinarVideo
from django.dispatch import receiver

@receiver(post_save, sender=WebinarVideo)
def process_uploaded_video(sender, instance, created, **kwargs):
    if created and instance.video:
        transaction.on_commit(
            lambda: process_video.delay(instance.pk)
        )