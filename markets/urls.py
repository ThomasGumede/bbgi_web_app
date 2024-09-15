from django.urls import path

from markets.views import create_service, delete_service, get_services, update_service, create_quotation

app_name = "markets"
urlpatterns = [
    path("service/create/business=<slug:listing_slug>", create_service, name="create-service"),
    path("<uuid:service_id>/update/business=<slug:listing_slug>", update_service, name="update-service"),
    path("<uuid:service_id>/delete/business=<slug:listing_slug>", delete_service, name="delete-service"),
    path("services/business=<slug:listing_slug>", get_services, name="get-services"),
    path("service=<uuid:service_id>/quote-request", create_quotation, name="create-quotation"),
]
