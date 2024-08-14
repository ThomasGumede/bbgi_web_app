from django.shortcuts import get_object_or_404
from listings.models import Business, Category
from django.db.models import Q
from django.db.models import Avg

def sort_listing(sort_by=None, province=None, bbee_level=None, query=None, place=None, category=None):
    listings = Business.objects.all()
    if category:
        category = get_object_or_404(Category, slug=category)
        listings = listings.filter(category=category)

    if province:
        
        listings = listings.filter(province__icontains=province)

    if bbee_level:
        
        listings = listings.filter(bbbee_level=bbee_level)

    if query:
        listings = listings.filter(Q(title__icontains=query) | Q(category__label__icontains=query) | Q(slogan__icontains=query) | Q(main_address__icontains=place or query))

    if sort_by:
        
        sorting_values = {
            "newest": listings.order_by("-created"),
            "best-rating": listings.annotate(avg_rating_value=Avg("reviews__rating_value")).order_by("-avg_rating_value"),
        }
        listings = sorting_values[str(sort_by)]

    return listings