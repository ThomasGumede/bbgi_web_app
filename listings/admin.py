from django.contrib import admin
from listings.models import *

from django.utils.html import format_html

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
    # Columns to display in list view
    list_display = ('title', 'owner', 'category', 'province', 'status', 'is_completed', 'phone', 'website')
    
    # Editable directly in list view
    list_editable = ('status', 'is_completed')
    
    # Filters in sidebar
    list_filter = ('status', 'category', 'province', 'is_completed')
    
    # Search fields
    search_fields = ('title', 'main_address', 'details', 'owner__username', 'email', 'phone')
    
    # Default ordering
    ordering = ('title',)
    
    # Group fields in collapsible sections
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'owner', 'category', 'logo', 'background_image', 'details', 'main_address', 'map_coordinates')
        }),
        ('Contact & Online', {
            'fields': ('website', 'email', 'phone', 'alternative_phone', 'facebook', 'twitter', 'instagram', 'linkedIn'),
            'classes': ('collapse',)
        }),
        ('Business Info', {
            'fields': ('bbbee_level', 'province', 'is_hours', 'hours_type', 'status', 'is_completed'),
            'classes': ('collapse',)
        }),
    )
    

  

@admin.register(ListingOrder)
class ListingOrderAdmin(admin.ModelAdmin):
    pass