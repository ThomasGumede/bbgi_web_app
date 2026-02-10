from django.db import models
from accounts.custom_models.abstracts import AbstractCreate
from events.models import EventModel
from campaigns.models import CampaignModel


class Coupon(AbstractCreate):
    discount = models.DecimalField(max_digits=1000, decimal_places=2, help_text="Discount amount for the coupon")
    code = models.CharField(max_length=50, unique=True, help_text="Unique code for the coupon")
    order_id = models.UUIDField(unique=True, null=True, blank=True)
    event = models.ForeignKey(EventModel, on_delete=models.CASCADE, null=True, blank=True, help_text="The event this coupon is associated with. Optional if the coupon is for a campaign.")
    campaign = models.ForeignKey(CampaignModel, on_delete=models.CASCADE, null=True, blank=True, help_text="The campaign this coupon is associated with. Optional if the coupon is for an event.")
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField()

    def __str__(self) -> str:
        return self.code
    
    def get_formated_date(self):
        return