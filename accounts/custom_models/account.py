from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_delete, post_save
import decimal
from accounts.custom_models.abstracts import AbstractCreate, AbstractPayment, AbstractProfile
from accounts.custom_models.choices import TITLE_CHOICES, WALLET_STATUS, PaymentStatus
from accounts.utilities.file_handlers import handle_profile_upload
from accounts.utilities.validators import verify_rsa_phone

PHONE_VALIDATOR = verify_rsa_phone()

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

    def get_full_name(self):
        if self.title:
            return f"{self.title} {self.first_name[0]} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"
        
    def get_absolute_url(self):
        return reverse("accounts:user-details", kwargs={"username": self.username})

class SubscriptionOrder(AbstractCreate, AbstractPayment):
    package = models.ForeignKey(SubscriptionPackage, null=True, blank=True, on_delete=models.SET_NULL, related_name="subscription_orders")
    subscriber = models.OneToOneField(Account, null=True, blank=True, on_delete=models.SET_NULL, related_name="subscription_order")
    order_id = models.CharField(max_length=150, editable=False, unique=True)

    client_first_name = models.CharField(max_length=250, null=True, blank=True)
    client_last_name = models.CharField(max_length=250, null=True, blank=True)
    client_phone = models.CharField(max_length=15, validators=[PHONE_VALIDATOR], null=True, blank=True)
    client_email = models.EmailField(null=True, blank=True)

    client_address_one = models.CharField(max_length=300, blank=True, null=True)
    client_address_two = models.CharField(max_length=300, blank=True, null=True)
    client_city = models.CharField(max_length=300, blank=True, null=True)
    client_province = models.CharField(max_length=300, blank=True, null=True)
    client_country = models.CharField(max_length=300, default="South Africa")
    client_zipcode = models.BigIntegerField(blank=True, null=True)

    vat = models.DecimalField(max_digits=1000, decimal_places=2)
    total_amount = models.DecimalField(max_digits=1000, decimal_places=2)
    discount = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    checkout_id = models.CharField(max_length=200, unique=True, null=True, blank=True, db_index=True)
    payment_status = models.CharField(max_length=40, choices=PaymentStatus.choices, default=PaymentStatus.NOT_PAID)

    def calculate_total_price(self):
        initial_amount = self.package.amount
        discount_amount = decimal.Decimal(initial_amount * decimal.Decimal((self.discount / 100)))
        discounted_amount = initial_amount - discount_amount
        self.total_amount = discounted_amount
        self.vat = decimal.Decimal(discounted_amount * decimal.Decimal((14/100)))

        return self.total_amount
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = f"BBGIS{timezone.now().strftime('%Y%m%dH%M%S')}{self.subscriber.id}"
        self.calculate_total_price()
        super(SubscriptionOrder, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Subscription Order")
        verbose_name_plural = _("Subscription Orders")
        ordering = ["-created"]

class AboutCompany(AbstractCreate, AbstractProfile):
    title = models.CharField(max_length=300, null=True, blank=True, unique=True)
    slogan = models.CharField(max_length=300, null=True, blank=True, unique=True)
    # vision = models.CharField(max_length=300, null=True, blank=True, unique=True)
    slug = models.SlugField(max_length=300, default="about-bbgi-model", unique=True)
    email = models.EmailField(null=True, blank=True)
    small_description = models.TextField(null=True, blank=True)
    vision = models.TextField(blank=True, null=True, unique=True)
    mission = models.TextField(blank=True, null=True, unique=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'About Company'
        verbose_name_plural = 'About Companys'