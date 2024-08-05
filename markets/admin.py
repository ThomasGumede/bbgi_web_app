from django.contrib import admin
from markets.models import Service, Qoutation
# Register your models here.

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass

@admin.register(Qoutation)
class QoutationAdmin(admin.ModelAdmin):
    pass