from django.urls import path
from markets.views.products import shop
from markets.views.quotation import create_quotation, qoutations, delete_quote, manage_quotations, get_qoutations, request_service
from markets.views.service import create_service, delete_service, get_services, update_service, service_details, add_service, all_services


app_name = "markets"
urlpatterns = [
    path("service/create/business=<slug:listing_slug>", create_service, name="create-service"),
    path("listing/<slug:listing_slug>/add-services", add_service, name="add-service"),
    path("dashboard/quotations", qoutations, name="qoutations"),
    path("markets/services", all_services, name="all-services"),
    path("markets/shop", shop, name="shop"),
    path("listing/manage/quotations/<slug:listing_slug>", get_qoutations, name="get-qoutations"),
    # path("quotes/get-service", request_service, name="request-qoutations"),
    path("account/quotations/manage", manage_quotations, name="manage-qoutations"),
    path("dashboard/quotations/<service_slug>/delete=<uuid:quotation_id>", delete_quote, name="delete-quote"),
    path("<uuid:service_id>/update/business=<slug:listing_slug>", update_service, name="update-service"),
    path("<uuid:service_id>/delete/business=<slug:listing_slug>", delete_service, name="delete-service"),
    path("services/business=<slug:listing_slug>", get_services, name="get-services"),
    path("services/service=<slug:service_slug>", service_details, name="service-details"),
    path("service=<uuid:service_id>/quote-request", create_quotation, name="create-quotation"),
]
