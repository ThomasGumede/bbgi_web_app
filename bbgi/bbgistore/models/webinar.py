from django.db import models
from ....bbgistore.models.abstract import StoreItem
class Webinar(StoreItem):
    duration=models.DurationField()
