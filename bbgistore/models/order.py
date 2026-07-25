from click import Path
from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import AbstractCreate
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.template.defaultfilters import slugify
from accounts.custom_models.abstracts import AbstractPayment
from bbgistore.models.book import Book, BookDownload
from bbgistore.models.webinar import Webinar
from campaigns.utils import generate_order_number

class BookOrder(AbstractCreate, AbstractPayment):
    order_number = models.CharField(max_length=300, editable=False, unique=True)
    checkout_id = models.CharField(max_length=200, unique=True, null=True, blank=True, db_index=True)
    client = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="book_orders",
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.PROTECT,
        related_name="orders",
    )
    quantity = models.PositiveIntegerField(default=1)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]
        constraints = [
            models.UniqueConstraint(
                fields=["client", "book"],
                name="unique_book_purchase",
            )
        ]

    @property
    def thumbnail(self):
        if self.book.thumbnail:
            return self.book.thumbnail.url
        return None
    
    @property
    def downloads(self):
        return BookDownload.objects.filter(
            user=self.client,
            book_file__book=self.book
        ).count()
    
    def save(self, *args, **kwargs):
        self.amount = self.book.price

        if not self.order_number:
            self.order_number = generate_order_number(BookOrder)

        super().save(*args, **kwargs)
    

    def __str__(self):
        return f"{self.client} - {self.book}"

class WebinarOrder(AbstractCreate, AbstractPayment):
    order_number = models.CharField(max_length=300, editable=False, unique=True)
    checkout_id = models.CharField(max_length=200, unique=True, null=True, blank=True, db_index=True)
    client = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="webinar_orders",
    )
    webinar = models.ForeignKey(
        Webinar,
        on_delete=models.PROTECT,
        related_name="orders",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Webinar Order"
        constraints = [
            models.UniqueConstraint(
                fields=["client", "webinar"],
                name="unique_webinar_purchase",
            )
        ]

    def save(self, *args, **kwargs):
        self.amount = self.webinar.price
        if not self.order_number:    
            self.order_number = generate_order_number(WebinarOrder)
        super(WebinarOrder, self).save(*args, **kwargs)

    
    def __str__(self):
        return f"{self.client} - {self.webinar}"
    
