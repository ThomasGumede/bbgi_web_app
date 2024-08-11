from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_delete, post_save

from accounts.custom_models.abstracts import AbstractCreate, AbstractPayment, AbstractProfile
from accounts.custom_models.choices import TITLE_CHOICES, WALLET_STATUS, PaymentStatus
from accounts.utilities.file_handlers import handle_profile_upload

class WalletModel(AbstractCreate):
    name = models.CharField(max_length=250)
    balance = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    owner = models.OneToOneField("Account", on_delete=models.CASCADE, related_name="my_wallet")
    status = models.CharField(max_length=150, choices=WALLET_STATUS, default=WALLET_STATUS[0])
    cleared_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _("Wallet")
        verbose_name_plural = _("Wallets")
        ordering = ["-created"]

    def request_payout_details(self):
        pass

    def clear_account(self):
        self.balance = 0

    def __str__(self):
        return self.name

class SubscriptionPackage(AbstractCreate):
    title = models.CharField(max_length=250, help_text=_("Enter subscription package title"))
    amount = models.DecimalField(default=0.0, max_digits=1000, decimal_places=2, help_text=_("Enter package price"))
    details = models.TextField(help_text=_("Enter package details"))
    max_businesses = models.IntegerField(default=1)
    max_services_per_business = models.IntegerField(default=5)
    max_products_per_business = models.IntegerField(default=5)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Package'
        verbose_name_plural = 'Packages'

class Account(AbstractUser, AbstractProfile):
    profile_image = models.ImageField(help_text=_("Upload profile image"), upload_to=handle_profile_upload, null=True, blank=True)
    title = models.CharField(max_length=30, choices=TITLE_CHOICES)
    maiden_name = models.CharField(help_text=_("Enter your maiden name"), max_length=300, blank=True, null=True)
    biography = models.TextField(blank=True)
    subscription = models.ForeignKey(SubscriptionPackage, related_name="subscribers", on_delete=models.SET_NULL, null=True, blank=True)
    is_technical = models.BooleanField(default=False)
    is_email_activated = models.BooleanField(default=False)
    is_paid = models.CharField(max_length=40, choices=PaymentStatus.choices, default=PaymentStatus.NOT_PAID)
    subscription_starts = models.DateTimeField(null=True, blank=True)
    subscription_ends = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")
        ordering = ["-created"]

    def __str__(self):
        return self.get_full_name()

class SubscriptionOrder(AbstractCreate, AbstractPayment):
    package = models.ForeignKey(SubscriptionPackage, null=True, blank=True, on_delete=models.SET_NULL, related_name="subscription_orders")
    subscriber = models.OneToOneField(Account, null=True, blank=True, on_delete=models.SET_NULL, related_name="subscription_order")
    order_id = models.CharField(max_length=150, editable=False, unique=True)
    vat = models.DecimalField(max_digits=1000, decimal_places=2)
    total_amount = models.DecimalField(max_digits=1000, decimal_places=2)
    checkout_id = models.CharField(max_length=200, unique=True, null=True, blank=True, db_index=True)
    payment_status = models.CharField(max_length=40, choices=PaymentStatus.choices, default=PaymentStatus.NOT_PAID)
    

    class Meta:
        verbose_name = _("Subscription Order")
        verbose_name_plural = _("Subscription Orders")
        ordering = ["-created"]