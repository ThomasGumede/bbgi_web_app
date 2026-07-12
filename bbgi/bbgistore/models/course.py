from django.db import models
from ....bbgistore.models.abstract import StoreItem
class Course(StoreItem):
    duration=models.DurationField()
