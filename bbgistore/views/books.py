from bbgistore.models.book import Book, BookFile
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required


def get_all_books(request):
    books = Book.objects.all()
    context = {
        "books": books
    }
    return render(request, "bbgistore/books/all-books.html", context)

def get_book_details(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug)
    context = {
        "book": book
    }
    return render(request, "bbgistore/books/book-details.html", context)