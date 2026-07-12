from django.db import models
from ....bbgistore.models.abstract import StoreItem
class Book(StoreItem):
    pages=models.PositiveIntegerField()
