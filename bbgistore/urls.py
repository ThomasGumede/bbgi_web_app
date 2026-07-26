from django.urls import path
from bbgistore.views.books import get_all_books, get_book_details, buy_book
from bbgistore.views.bbgi_store import bbgi_store
from bbgistore.views.webinars import all_webinars, get_webinar_details

app_name = "bbgistore"

urlpatterns = [
    path("bbgi-store/digital-store", bbgi_store, name="bbgi-store"),
    path("bbgi-store/books/", get_all_books, name="all_books"),
    path("bbgi-store/books/<slug:book_slug>/", get_book_details, name="book_details"),
    path("bbgi-store/webinars/", all_webinars, name="all_webinars"),
    path("bbgi-store/webinars/<slug:webinar_slug>/", get_webinar_details, name="webinar_details"),
    
    # Orders
    path("bbgi-store/order-book/<slug:book_slug>/", buy_book, name="order-book"),
    path("bbgi-store/register-for-webinar/<slug:webinar_slug>/", buy_book, name="register-for-webinar"),
]
