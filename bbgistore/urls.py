from django.urls import path
from bbgistore.views.books import get_all_books, get_book_details
from bbgistore.views.bbgi_store import bbgi_store

app_name = "bbgistore"

urlpatterns = [
    path("bbgi-store/digital-store", bbgi_store, name="bbgi-store"),
    path("bbgi-store/books/", get_all_books, name="all_books"),
    path("bbgi-store/books/<slug:book_slug>/", get_book_details, name="book_details"),
]
