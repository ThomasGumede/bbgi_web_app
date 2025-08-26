from django.urls import path
from listings.views.business_hours import get_business_hours, update_business_hour, add_business_hours, update_business_hours
from listings.views.business_lcation import create_location, delete_location, get_locations, update_location, add_main_location, update_main_location
from listings.views.business_order import order_subscription, cancel_listing_order
from listings.views.business_views import add_listing, add_listing_socials, delete_listing, \
    delete_listing_content, get_business_hours_api, get_listing, get_listings, manage_listing, \
        manage_listings, update_listing, update_listing_content, get_started_with_listing, update_listing_socials


app_name = "listings"

urlpatterns = [
    path("businesses/", get_listings, name="listings"),
    path("account/listings/manage", manage_listings, name="manage-listings"),
    path("listings/category=<slug:category>", get_listings, name="get-listings-by-category"),
    path("business/<slug:listing_slug>", get_listing, name="get-listing"),
    path("listing/create-listing", add_listing, name = "add-listing"),
    path("listing/<slug:listing_slug>/create-listing", add_listing, name = "add-listing-with-slug"),
    path("listing/<slug:listing_slug>/create-listing-hours", add_business_hours, name = "add-business-hours"),
    path("listing/<slug:listing_slug>/add-contact-info", add_listing_socials, name = "add-business-socials"),
    path("listing/<slug:listing_slug>/add-main-location", add_main_location, name = "add-business-main-location"),
    path("listing/<slug:listing_slug>/payment-checkout", order_subscription, name = "order-subscription"),
    path("listing/<uuid:order_id>/cancel-payment-checkout", cancel_listing_order, name = "cancel-listing-order"),

    
    path("listing/get-started", get_started_with_listing, name = "get-started-with-listing"),
    path("listing/manage/delete/<slug:listing_slug>", delete_listing, name="delete-listing"),
    path("listing/manage/update/<slug:listing_slug>", update_listing, name="update-listing"),
    path("listing/manage/update-content/<slug:listing_slug>", update_listing_content, name="update-listing-content"),
    path("listing/manage/update-main-location/<slug:listing_slug>", update_main_location, name="update-main-location"),
    path("listing/manage/update-listing-socials/<slug:listing_slug>", update_listing_socials, name="update-listing-socials"),
    path("listing/manage/locations/<slug:listing_slug>", get_locations, name="get-locations"),
    path("listing/manage/add-busines-location/<slug:listing_slug>", create_location, name="create-location"),
    path("listing/manage/update-business-location/<uuid:location_id>", update_location, name="update-location"),
    path("listing/manage/delete-business-location/<uuid:location_id>", delete_location, name="delete-location"),
    path("dashboard/delete/content/<slug:listing_slug>/<uuid:content_id>", delete_listing_content, name="delete-listing-content"),
    path("listing/manage/<slug:listing_slug>", manage_listing, name="manage-listing"),
    path("listing/manage/business-hours/<slug:listing_slug>", get_business_hours, name="get-business-hours"),
    path("listing/manage/update-business-hours/<slug:listing_slug>", update_business_hours, name="update-listing-hours-big"),
    path("listing/manage/update-business-hours/<slug:listing_slug>/<uuid:hour_id>", update_business_hour, name="update-business-hour"),

    # API URLS
    path("api/hours/<uuid:listing_id>", get_business_hours_api, name="get-business-hours-api")
]