from django.contrib import admin
from payments.models import BBGIBankModel, PaymentInformation
from events.models import TicketOrderModel
from bbgistore.models.order import BookOrder, WebinarOrder
from campaigns.models import ContributionModel
from django.utils.html import format_html

@admin.register(BBGIBankModel)
class BBGIBankBankAdmin(admin.ModelAdmin):
    list_display = ('balance', 'order_uuid', 'order_id', 'tip', 'received_at')

@admin.register(PaymentInformation)
class PaymentInformation(admin.ModelAdmin):
    list_display = ('order_number', 'order_updated')

@admin.register(WebinarOrder)
class WebinarOrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "webinar_thumbnail",
        "webinar",
        "client",
        "amount",
        "paid_badge",
        "payment_method_type",
        "payment_date",
        "created",
    )

    list_display_links = (
        "order_number",
        "webinar",
    )

    list_filter = (
        "paid",
        "payment_method_type",
        "payment_date",
        "created",
    )

    search_fields = (
        "order_number",
        "checkout_id",
        "client__username",
        "client__first_name",
        "client__last_name",
        "client__email",
        "webinar__title",
    )

    autocomplete_fields = (
        "client",
        "webinar",
    )

    readonly_fields = (
        "order_number",
        "checkout_id",
        "payment_method_type",
        "payment_method_card_holder",
        "payment_method_masked_card",
        "payment_method_scheme",
        "payment_date",
        "amount",
        "thumbnail_preview",
        "created",
        "updated",
    )

    ordering = (
        "-created",
    )

    list_per_page = 30

    save_on_top = True

    date_hierarchy = "created"

    actions = (
        "mark_paid",
        "mark_unpaid",
    )

    fieldsets = (
        (
            "Order Information",
            {
                "fields": (
                    "order_number",
                    "checkout_id",
                    "client",
                    "webinar",
                    "amount",
                    "paid",
                )
            },
        ),
        (
            "Webinar",
            {
                "fields": (
                    "thumbnail_preview",
                )
            },
        ),
        (
            "Payment Information",
            {
                "classes": ("collapse",),
                "fields": (
                    "payment_method_type",
                    "payment_method_card_holder",
                    "payment_method_masked_card",
                    "payment_method_scheme",
                    "payment_date",
                )
            },
        ),
        (
            "System Information",
            {
                "classes": ("collapse",),
                "fields": (
                    "created",
                    "updated",
                )
            },
        ),
    )

    @admin.display(description="Thumbnail")
    def webinar_thumbnail(self, obj):
        if obj.webinar.thumbnail:
            return format_html(
                '<img src="{}" style="height:55px;width:85px;object-fit:cover;border-radius:6px;">',
                obj.webinar.thumbnail.url,
            )
        return "-"

    @admin.display(description="Preview")
    def thumbnail_preview(self, obj):
        if obj.webinar.thumbnail:
            return format_html(
                '<img src="{}" style="max-height:220px;border-radius:8px;">',
                obj.webinar.thumbnail.url,
            )
        return "No thumbnail uploaded."

    @admin.display(boolean=True, description="Paid")
    def paid_badge(self, obj):
        return obj.paid

    @admin.action(description="Mark selected orders as paid")
    def mark_paid(self, request, queryset):
        updated = 0

        for order in queryset:
            if not order.paid:
                order.mark_paid() if hasattr(order, "mark_paid") else setattr(order, "paid", True)
                if not hasattr(order, "mark_paid"):
                    order.save(update_fields=["paid"])
                updated += 1

        self.message_user(
            request,
            f"{updated} webinar order(s) marked as paid."
        )

    @admin.action(description="Mark selected orders as unpaid")
    def mark_unpaid(self, request, queryset):
        updated = queryset.update(paid=False)

        self.message_user(
            request,
            f"{updated} webinar order(s) marked as unpaid."
        )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "client",
                "webinar",
            )
        )

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))

        if obj and obj.paid:
            readonly.extend([
                "client",
                "webinar",
                "paid",
            ])

        return readonly
    
@admin.register(BookOrder)
class BookOrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "book_cover",
        "book",
        "client",
        "quantity",
        "amount",
        "paid_badge",
        "payment_method_type",
        "payment_date",
        "created",
    )

    list_display_links = (
        "order_number",
        "book",
    )

    list_filter = (
        "paid",
        "payment_method_type",
        "created",
        "payment_date",
    )

    search_fields = (
        "order_number",
        "checkout_id",
        "client__username",
        "client__first_name",
        "client__last_name",
        "client__email",
        "book__title",
    )

    autocomplete_fields = (
        "client",
        "book",
    )

    readonly_fields = (
        "order_number",
        "checkout_id",
        "payment_method_type",
        "payment_method_card_holder",
        "payment_method_masked_card",
        "payment_method_scheme",
        "payment_date",
        "amount",
        "cover_preview",
        "created",
        "updated",
    )

    ordering = (
        "-created",
    )

    list_per_page = 30

    save_on_top = True

    date_hierarchy = "created"

    actions = (
        "mark_paid",
        "mark_unpaid",
    )

    fieldsets = (
        (
            "Order Information",
            {
                "fields": (
                    "order_number",
                    "checkout_id",
                    "client",
                    "book",
                    "quantity",
                    "amount",
                    "paid",
                )
            },
        ),
        (
            "Book",
            {
                "fields": (
                    "cover_preview",
                )
            },
        ),
        (
            "Payment Details",
            {
                "classes": ("collapse",),
                "fields": (
        
        
        
                    "payment_method_type",
                    "payment_method_card_holder",
                    "payment_method_masked_card",
                    "payment_method_scheme",
                    "payment_date",
                )
            },
        ),
        (
            "System",
            {
                "classes": ("collapse",),
                "fields": (
                    "created",
                    "updated",
                )
            },
        ),
    )

    @admin.display(description="Cover")
    def book_cover(self, obj):
        if obj.book.thumbnail:
            return format_html(
                '<img src="{}" style="height:55px;width:40px;object-fit:cover;border-radius:6px;">',
                obj.book.thumbnail.url,
            )
        return "-"

    @admin.display(description="Preview")
    def cover_preview(self, obj):
        if obj.book.thumbnail:
            return format_html(
                '<img src="{}" style="max-height:220px;border-radius:8px;">',
                obj.book.thumbnail.url,
            )
        return "No cover available."

    @admin.display(boolean=True, description="Paid")
    def paid_badge(self, obj):
        return obj.paid

    @admin.action(description="Mark selected orders as paid")
    def mark_paid(self, request, queryset):
        updated = queryset.update(paid=True)
        self.message_user(
            request,
            f"{updated} order(s) marked as paid."
        )

    @admin.action(description="Mark selected orders as unpaid")
    def mark_unpaid(self, request, queryset):
        updated = queryset.update(paid=False)
        self.message_user(
            request,
            f"{updated} order(s) marked as unpaid."
        )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "client",
                "book",
            )
        )
