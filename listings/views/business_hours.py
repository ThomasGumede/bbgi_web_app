from listings.forms import BusinessHourForm, BusinessLocationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from listings.models import Business, BusinessLocation, BusinessHour
from django.contrib import messages


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
