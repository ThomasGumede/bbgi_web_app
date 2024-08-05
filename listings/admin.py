from django.contrib import admin
from listings.models import *

@admin.register(BusinessReview)
class BusinessReviewAdmin(admin.ModelAdmin):
    pass

@admin.register(BusinessContent)
class BusinessContentAdmin(admin.ModelAdmin):
    pass

@admin.register(BusinessHour)
class BusinessHourAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    pass