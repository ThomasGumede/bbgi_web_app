# Generated by Django 4.2.5 on 2025-01-01 00:13

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import events.models
import tinymce.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bbgi_home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventModel',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, help_text='Upload campaign image.', null=True, upload_to=events.models.handle_event_file_upload)),
                ('title', models.CharField(help_text='Enter title for your event', max_length=150)),
                ('slug', models.SlugField(blank=True, max_length=250, unique=True)),
                ('phone', models.CharField(help_text='Enter cellphone number', max_length=15, validators=[django.core.validators.RegexValidator('^(\\+27|0)[1-9][0-9]{8}$', 'RSA phone number is required')])),
                ('email', models.EmailField(max_length=254)),
                ('small_description', models.TextField(blank=True, help_text='Small description about your event for search', null=True)),
                ('content', tinymce.models.HTMLField()),
                ('venue_name', models.CharField(blank=True, help_text='Enter event venue name', max_length=400, null=True)),
                ('event_address', models.CharField(blank=True, help_text='Enter event address seperated by comma', max_length=300, null=True)),
                ('map_coordinates', models.CharField(blank=True, max_length=300, null=True)),
                ('total_seats_sold', models.PositiveIntegerField(default=0)),
                ('event_link', models.URLField(blank=True, null=True)),
                ('event_startdate', models.DateTimeField(validators=[django.core.validators.MinValueValidator(datetime.datetime(2025, 1, 1, 0, 13, 55, 767176, tzinfo=datetime.timezone.utc), 'Event start date and time cannot be in the past')])),
                ('event_enddate', models.DateTimeField(validators=[django.core.validators.MinValueValidator(datetime.datetime(2025, 1, 1, 0, 13, 55, 767227, tzinfo=datetime.timezone.utc), 'Event end date and time cannot be in the past')])),
                ('status', models.CharField(choices=[('NOT APPROVED', 'Not approved'), ('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('Completed', 'Completed'), ('Blocked', 'Blocked')], default='NOT APPROVED', max_length=50)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='events', to='bbgi_home.blogcategory')),
                ('organiser', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.CreateModel(
            name='EventTicketTypeModel',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(help_text='Enter ticket type', max_length=250)),
                ('available_seats', models.PositiveIntegerField(default=0)),
                ('sale_start', models.DateTimeField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(datetime.datetime(2025, 1, 1, 0, 13, 55, 772877, tzinfo=datetime.timezone.utc), 'Ticket sale start date and time cannot be in the past')])),
                ('sale_end', models.DateTimeField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(datetime.datetime(2025, 1, 1, 0, 13, 55, 772909, tzinfo=datetime.timezone.utc), 'Ticket sale end date and time cannot be in the past')])),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=1000)),
                ('transaction_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=1000)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=1000)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickettypes', to='events.eventmodel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TicketOrderModel',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('payment_method_type', models.CharField(blank=True, max_length=50, null=True)),
                ('payment_method_card_holder', models.CharField(blank=True, max_length=50, null=True)),
                ('payment_method_masked_card', models.CharField(blank=True, max_length=50, null=True)),
                ('payment_method_scheme', models.CharField(blank=True, max_length=50, null=True)),
                ('payment_date', models.CharField(blank=True, max_length=50, null=True)),
                ('order_number', models.CharField(editable=False, max_length=300, unique=True)),
                ('checkout_id', models.CharField(blank=True, db_index=True, max_length=200, null=True, unique=True)),
                ('client_first_name', models.CharField(blank=True, max_length=250, null=True)),
                ('client_last_name', models.CharField(blank=True, max_length=250, null=True)),
                ('client_phone', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator('^(\\+27|0)[1-9][0-9]{8}$', 'RSA phone number is required')])),
                ('client_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('client_address_one', models.CharField(blank=True, max_length=300, null=True)),
                ('client_address_two', models.CharField(blank=True, max_length=300, null=True)),
                ('client_city', models.CharField(blank=True, max_length=300, null=True)),
                ('client_province', models.CharField(blank=True, max_length=300, null=True)),
                ('client_country', models.CharField(default='South Africa', max_length=300)),
                ('client_zipcode', models.BigIntegerField(blank=True, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('coupon_code', models.CharField(blank=True, max_length=300, null=True)),
                ('quantity', models.PositiveBigIntegerField(default=1)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=1000)),
                ('order_note', models.TextField(blank=True, null=True)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=1000)),
                ('total_transaction_costs', models.DecimalField(decimal_places=2, default=0.0, max_digits=1000)),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=1000)),
                ('tip', models.DecimalField(decimal_places=2, default=0.0, max_digits=1000)),
                ('accepted_laws', models.BooleanField(default=True)),
                ('reservation_time', models.TimeField(default=events.models.reservation_time)),
                ('paid', models.CharField(choices=[('PAID', 'Paid'), ('PENDING', 'Pending'), ('NOT PAID', 'Not paid'), ('CANCELLED', 'Cancelled')], default='NOT PAID', max_length=300)),
                ('receipt', models.FileField(null=True, upload_to='tickets/invoice/')),
                ('tickets_pdf_file', models.FileField(null=True, upload_to='tickets/pdf/')),
                ('buyer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ticketorders', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_orders', to='events.eventmodel')),
            ],
            options={
                'verbose_name': 'Ticker order',
                'verbose_name_plural': 'Ticker orders',
            },
        ),
        migrations.CreateModel(
            name='TicketModel',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('guest_full_name', models.CharField(blank=True, max_length=300, null=True)),
                ('guest_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('guest_phone_number', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator('^(\\+27|0)[1-9][0-9]{8}$', 'RSA phone number is required')])),
                ('quantity', models.PositiveBigIntegerField()),
                ('barcode_value', models.CharField(blank=True, max_length=13, null=True, unique=True)),
                ('barcode_image', models.ImageField(blank=True, null=True, upload_to='tickets/barcodes/')),
                ('qrcode_url', models.URLField(blank=True, null=True)),
                ('qrcode_image', models.ImageField(blank=True, null=True, upload_to='tickets/qrcodes/')),
                ('scanned', models.BooleanField(default=False)),
                ('scanned_at', models.DateTimeField(blank=True, null=True)),
                ('ticket_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='events.ticketordermodel')),
                ('ticket_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='events.eventtickettypemodel')),
            ],
            options={
                'verbose_name': 'Ticket',
                'verbose_name_plural': 'Tickets',
            },
        ),
        
        migrations.CreateModel(
            name='EventOrganisor',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('full_name', models.CharField(max_length=350)),
                ('organisor_phone_one', models.CharField(blank=True, max_length=15, null=True, unique=True, validators=[django.core.validators.RegexValidator('^(\\+27|0)[1-9][0-9]{8}$', 'RSA phone number is required')])),
                ('organisor_email', models.EmailField(max_length=254)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organisors', to='events.eventmodel')),
            ],
            options={
                'verbose_name': 'Event Organisor',
                'verbose_name_plural': 'Event Organisors',
                'unique_together': {('full_name', 'organisor_phone_one', 'organisor_email')},
            },
        ),
    ]