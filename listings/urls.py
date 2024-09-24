from django.urls import path
from listings.views.business_hours import get_business_hours, update_business_hour, add_business_hours
from listings.views.business_lcation import create_location, delete_location, get_locations, update_location, add_main_location
from listings.views.business_views import add_listing, add_listing_socials, delete_listing, delete_listing_content, get_business_hours_api, get_listing, get_listings, manage_listing, manage_listings, update_listing, update_listing_content, get_started_with_listing


app_name = "listings"

urlpatterns = [
    path("listings/", get_listings, name="listings"),
    path("dashboard/listings/manage", manage_listings, name="manage-listings"),
    path("listings/category=<slug:category>", get_listings, name="get-listings-by-category"),
    path("listing/details/<slug:listing_slug>", get_listing, name="get-listing"),
    path("listing/create-listing", add_listing, name = "add-listing"),
    path("listing/<slug:listing_slug>/create-listing", add_listing, name = "add-listing-with-slug"),
    path("listing/<slug:listing_slug>/create-listing-hours", add_business_hours, name = "add-business-hours"),
    path("listing/<slug:listing_slug>/add-contact-info", add_listing_socials, name = "add-business-socials"),
    path("listing/<slug:listing_slug>/add-main-location", add_main_location, name = "add-business-main-location"),

    
    path("listing/get-started", get_started_with_listing, name = "get-started-with-listing"),
    path("dashboard/listing/delete/<slug:listing_slug>", delete_listing, name="delete-listing"),
    path("dashboard/listing/update/<slug:listing_slug>", update_listing, name="update-listing"),
    path("dashboard/listing/update/content/<slug:listing_slug>", update_listing_content, name="update-listing-content"),
    path("dashboard/listing/update/locations/<slug:listing_slug>", get_locations, name="get-locations"),
    path("dashboard/listing/update/locations/create/<slug:listing_slug>", create_location, name="create-location"),
    path("dashboard/listing/update/locations/update/<uuid:location_id>", update_location, name="update-location"),
    path("dashboard/listing/update/locations/delete/<uuid:location_id>", delete_location, name="delete-location"),
    path("dashboard/delete/content/<slug:listing_slug>/<uuid:content_id>", delete_listing_content, name="delete-listing-content"),
    path("dashboard/manage/<slug:listing_slug>", manage_listing, name="manage-listing"),
    path("dashboard/listing/update/business-hours/<slug:listing_slug>", get_business_hours, name="get-business-hours"),
    path("dashboard/listing/update/business-hours/<slug:listing_slug>/<uuid:hour_id>", update_business_hour, name="update-business-hour"),

    # API URLS
    path("api/hours/<uuid:listing_id>", get_business_hours_api, name="get-business-hours-api")
]