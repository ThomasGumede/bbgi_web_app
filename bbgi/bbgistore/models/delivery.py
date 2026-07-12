from django.db import models
class DeliveryMethod(models.Model):
    name=models.CharField(max_length=100)
    fee=models.DecimalField(max_digits=10,decimal_places=2)
    estimated_delivery_days=models.PositiveIntegerField()
