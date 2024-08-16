from listings.forms import BusinessLocationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from listings.models import Business, BusinessLocation, BusinessHour
from django.contrib import messages


@login_required
def get_business_hours(request, listing_id):
    queryset = Business.objects.all().prefetch_related("business_hours")
    listing = get_object_or_404(queryset, id=listing_id, owner=request.user)
    return render(request, "business/hours/get-business-hours.html", {"listing": listing})
