from listings.forms import BusinessHourForm, BusinessLocationForm
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from listings.models import Business, BusinessLocation, BusinessHour
from django.contrib import messages

@login_required
def add_business_hours(request, listing_slug):
    listing = get_object_or_404(Business, slug=listing_slug, owner=request.user)

    

    business_hour_forms = formset_factory(BusinessHourForm, extra=7, max_num=7)
    if request.method == "POST":
        if listing.business_hours.count() > 0:
            for hour in listing.business_hours.all():
                hour.delete()
                
        forms = business_hour_forms(request.POST)
        if forms.is_valid():

            for hours in forms:
                business_hours = hours.save(commit=False)
                business_hours.business = listing
                business_hours.save()
            
            messages.success(request, "Business listed successfully. It will take 2 - 4 hours to verify your business. For now, you can manage your business. Thank you")
            return redirect("listings:manage-listing", listing_slug=listing.slug)
        else:
            messages.error(request, "Something went wrong while trying to add your business hours")
            return render(request, "business/create-listing/add-hours.html", {"listing": listing, "forms": forms})
        
    
    return render(request, "business/create-listing/add-hours.html", {"listing": listing, "forms": business_hour_forms})

@login_required
def get_business_hours(request, listing_slug):
    queryset = Business.objects.all().prefetch_related("business_hours")
    listing = get_object_or_404(queryset, slug=listing_slug, owner=request.user)
    return render(request, "business/hours/get-business-hours.html", {"listing": listing})

@login_required
def update_business_hour(request, listing_slug, hour_id):
    queryset = Business.objects.all().prefetch_related("business_hours")
    listing = get_object_or_404(queryset, slug=listing_slug, owner=request.user)
    hour = get_object_or_404(BusinessHour, id=hour_id)
    if request.method == "POST":
        form = BusinessHourForm(instance=hour, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Business Hour successfully updated")
            return redirect("listings:get-business-hours", listing.slug)
        else:
            messages.error(request, "Something went wrong trying to update business hour")
            return render(request, "business/hours/update-business-hour.html", {"form": form, "hour": hour, "listing": listing})

    form = BusinessHourForm(instance=hour)
    return render(request, "business/hours/update-business-hour.html", {"form": form, "hour": hour, "listing": listing})
