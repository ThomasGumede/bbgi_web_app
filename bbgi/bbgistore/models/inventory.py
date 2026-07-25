from django.db import models
class Inventory(models.Model):
    stock=models.PositiveIntegerField(default=0)
