from django.urls import path

from listings.views import add_listing, delete_listing, delete_listing_content, get_business_hours_api, get_listing, get_listings, manage_listing, manage_listings, update_listing, update_listing_content


app_name = "listings"

urlpatterns = [
    path("listings/", get_listings, name="listings"),
    path("manage", manage_listings, name="manage-listings"),
    path("listings/category=<slug:category>", get_listings, name="get-listings-by-category"),
    path("listing/details/<slug:listing_slug>", get_listing, name="get-listing"),
    path("listing/delete/<uuid:listing_id>", delete_listing, name="delete-listing"),
    path("listing/update/<uuid:listing_id>", update_listing, name="update-listing"),
    path("listing/update/content/<uuid:listing_id>", update_listing_content, name="update-listing-content"),
    path("delete/content/<uuid:listing_id>/<uuid:content_id>", delete_listing_content, name="delete-listing-content"),
    path("manage/<slug:listing_slug>", manage_listing, name="manage-listing"),
    path("add", add_listing, name = "add-listing"),

    # API URLS
    path("api/hours/<uuid:listing_id>", get_business_hours_api, name="get-business-hours-api")
]