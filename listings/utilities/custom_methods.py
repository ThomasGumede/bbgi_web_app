from django.shortcuts import get_object_or_404
from listings.models import Business, Category
from django.db.models import Q
from django.db.models import Avg

def sort_listing(sort_by=None, province=None, bbee_level=None, query=None, place=None, category=None, tag=None):
    """
    Filter and sort business listings based on provided parameters.
    
    Args:
        sort_by (str): Sorting option ('newest', 'oldest', 'best-rating', 'title_asc', 'title_desc')
        province (str): Province filter
        bbee_level (str): BBBEE level filter
        query (str): General search query
        place (str): Location-specific search (used for main_address if provided)
        category (str): Category slug
        tag (str): Tag name or slug
    
    Returns:
        QuerySet: Filtered and sorted Business queryset
    """
    listings = Business.objects.all()
    
    if category:
        category = get_object_or_404(Category, slug=category)
        listings = listings.filter(category=category)

    if province:
        listings = listings.filter(province__icontains=province)

    if bbee_level:
        listings = listings.filter(bbbee_level=bbee_level)

    if query:
        listings = listings.filter(
            Q(title__icontains=query) | 
            Q(tags__name__icontains=query) | 
            Q(category__label__icontains=query) | 
            Q(slogan__icontains=query) | 
            Q(main_address__icontains=place or query)
        )

    if tag:
        listings = listings.filter(Q(tags__name__icontains=tag) | Q(tags__slug__icontains=tag))

    if sort_by == "newest":
        listings = listings.order_by("-created")
    elif sort_by == "oldest":
        listings = listings.order_by("created")
    elif sort_by == "best-rating":
        listings = listings.annotate(avg_rating_value=Avg("reviews__rating_value")).order_by("-avg_rating_value", "-created")
    elif sort_by == "title_asc":
        listings = listings.order_by("title")
    elif sort_by == "title_desc":
        listings = listings.order_by("-title")
    else:
        # Default to newest if invalid sort_by
        listings = listings.order_by("-created")

    return listings.distinct()