from listings.forms import BusinessLocationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from listings.models import Business, BusinessLocation
from django.contrib import messages

@login_required
def get_locations(request, listing_id):
    queryset = Business.objects.all().prefetch_related("business_locations")
    listing = get_object_or_404(queryset, id=listing_id, owner=request.user)
    return render(request, "business/location/get-locations.html", {"listing": listing})

@login_required
def create_location(request, listing_id):
    queryset = Business.objects.all().prefetch_related("business_locations")
    listing = get_object_or_404(queryset, id=listing_id, owner=request.user)
    if request.method == "POST":
        form = BusinessLocationForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.business = listing
            location.save()
            messages.success(request, "Successfully added new business location")
            return redirect("listings:get-locations", listing.id)
        else:
            messages.error(request, "Error trying to save your business location")
            return render(request, "business/location/create-location.html", {"listing": listing, "form": form})
        
    form = BusinessLocationForm()
    return render(request, "business/location/create-location.html", {"listing": listing, "form": form})

@login_required
def update_location(request, location_id):
    queryset = Business.objects.all().select_related("category").prefetch_related("business_locations", "reviews", "images")
    location = get_object_or_404(BusinessLocation, id=location_id)
    listing = get_object_or_404(queryset, id=location.business.id, owner=request.user)
    
    if request.method == "POST":
        form = BusinessLocationForm(data=request.POST, instance=location)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully updated business location")
            return redirect("listings:get-locations", listing.id)
        else:
            messages.error(request, "Error trying to update your business location")
            return render(request, "business/location/update-location.html", {"listing": listing, "form": form})
        
    form = BusinessLocationForm(instance=location)
    return render(request, "business/location/update-location.html", {"listing": listing, "form": form})

@login_required
def delete_location(request, location_id):
    queryset = Business.objects.all().select_related("category").prefetch_related("business_locations", "reviews", "images")
    location = get_object_or_404(BusinessLocation, id=location_id)
    listing = get_object_or_404(queryset, id=location.business.id, owner=request.user)
    
    if location.delete():
        messages.success(request, "Successfully deleted business location")
        return redirect("listings:get-locations", listing.id)
    else:
        messages.error(request, "Error trying to update your business location")
        return render(request, "business/location/update-location.html", {"listing": listing})
        