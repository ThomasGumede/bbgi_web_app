from bbgistore.models.book import Book
from bbgistore.models.webinar import Webinar
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def bbgi_store(request):
    search_query = request.GET.get("q", "")
    type_filter = request.GET.get("type", "")
    if search_query:
        if type_filter == "book":
            books = Book.objects.filter(Q(title__icontains=search_query) | Q(short_description__icontains=search_query), is_active=True, status="published").order_by("-created")
            context = {
                "books": books,
                "search_query": search_query,
                "type_filter": type_filter,
            }
            return render(request, 'bbgistore/books/all-books.html', context)
        elif type_filter == "webinar":
            webinars = Webinar.objects.filter(Q(title__icontains=search_query) | Q(short_description__icontains=search_query), is_active=True, status="published").order_by("-created")
            context = {
                "webinars": webinars,
                "search_query": search_query,
                "type_filter": type_filter,
            }
            return render(request, 'bbgistore/webinars/all-webinars.html', context)
        
    context = {
        "books": Book.objects.filter(is_active=True, status="published").order_by("-created")[:5],
        "webinars": Webinar.objects.filter(is_active=True, status="published").order_by("-created"),
    }
    return render(request, 'bbgistore/bbgi-store.html', context)


@login_required
def bbgi_store_dashboard(request):
    context = {
        "books": Book.objects.filter(is_active=True, status="published").order_by("-created")[:5],
        "webinars": Webinar.objects.filter(is_active=True, status="published").order_by("-created"),
    }
    return render(request, 'bbgistore/bbgi-store-dashboard.html', context)
