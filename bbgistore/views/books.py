from bbgistore.models.book import Book
from bbgistore.models.abstract import StoreCategory
from payments.ordermodels.storeorder import BookOrder
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required


def get_all_books(request, category_slug=None):
    books = Book.objects.filter(status="published").order_by('-created')
    query = request.GET.get("q", None)
    if category_slug:
        category = get_object_or_404(StoreCategory, slug=category_slug)
        books = books.filter(category=category)
    
    if query:
        books = books.filter(title__icontains=query) 
           
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

@login_required
def buy_book(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug)
    try:
        bookorder = BookOrder.objects.get(client=request.user, paid=False)
    except BookOrder.DoesNotExist:
        bookorder = BookOrder.objects.create(client=request.user, book=book, amount=book.price)
        
    return redirect('payments:book-payment', bookorder.id)