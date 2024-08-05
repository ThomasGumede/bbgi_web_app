import logging
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from bbgi_home.utilities.decorators import user_not_superuser_or_staff
from django.contrib.auth import get_user_model
from django.db.models import Q

from listings.models import Business, Category

USER = get_user_model()

@login_required
@user_not_superuser_or_staff
def all_accounts(request):
    template = "dashboard/accounts/users.html"
    query = request.GET.get("q", None)
    users = USER.objects.all()
    if query:
        users = USER.objects.filter(
            Q(username__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query) 
            | Q(address_one__icontains = query)
        )
        
    return render(request, "dashboard/accounts/all-accounts.html", {"accounts": users, "query": query})

@login_required
@user_not_superuser_or_staff
def all_listings(request, category=None):
    
    query = request.GET.get("query", None)
    listings = Business.objects.all()
    categories = Category.objects.all()
    if category:
        category = get_object_or_404(categories, slug=category)
        listings = listings.filter(category=category)
    
    if query:
        listings = listings.filter(Q(title__icontains=query) | Q(category__label__icontains=query) | Q(slogan__icontains=query))
        
    return render(request, "dashboard/listings/all-listings.html", {"listings": listings, "query": query})

@login_required
@user_not_superuser_or_staff
def delete_listing(request, listing_id):
    listing = get_object_or_404(Business, id=listing_id)
    if request.method == "POST":
        listing.delete()
        messages.success(request, "Listing deleted successfully")
        return redirect("bbgi_home:all-listings")
    return render(request, "dashboard/listings/delete-listing.html")


