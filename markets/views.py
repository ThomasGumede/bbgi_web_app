from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from listings.models import Business
from markets.models import Service, Qoutation
from markets.forms import ServiceForm, QoutationForm
from django.contrib import messages

@login_required
def get_services(request, listing_id):
    listing = get_object_or_404(Business, id=listing_id, owner=request.user)
    services = Service.objects.filter(business = listing)
    return render(request, "markets/services/services.html", {"listing": listing, "services": services})

@login_required
def create_service(request, listing_id):
    listing = get_object_or_404(Business, id=listing_id, owner=request.user)
    form = ServiceForm()

    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid() and form.is_multipart():
            service = form.save(commit=False)
            service.business = listing
            service.save()
            messages.success(request, "Service added successfully")
            return redirect("markets:get-services", listing.id)
        else:
            messages.error(request, "Error trying to create service")
            return render(request, "markets/services/create-service.html", {"form": form})
        
    return render(request, "markets/services/create-service.html", {"form": form, "listing": listing})

@login_required
def update_service(request, listing_id, service_id):
    listing = get_object_or_404(Business, id=listing_id, owner=request.user)
    service = get_object_or_404(Service, id=service_id, business=listing)
    form = ServiceForm(instance=service)

    if request.method == "POST":
        form = ServiceForm(instance=service, data=request.POST, files=request.FILES)
        if form.is_valid() and form.is_multipart():
            service.save()
            messages.success(request, "Service updated successfully")
            return redirect("markets:get-services", listing.id)
        else:
            messages.error(request, "Error trying to update service")
            return render(request, "markets/services/update-service.html", {"form": form})
        
    return render(request, "markets/services/update-service.html", {"form": form, "listing": listing})

@login_required
def delete_service(request, listing_id, service_id):
    listing = get_object_or_404(Business, id=listing_id, owner=request.user)
    service = get_object_or_404(Service, id=service_id, business=listing)
    if request.method == "POST":
        service.delete()
        messages.success(request, "Service was deleted successfully")
        return redirect("markets:get-services", listing.id)
    return render(request, "markets/services/delete-service.html", {"listing": listing, "service": service})


@login_required
def create_quotation(request, service_id):
    
    service = get_object_or_404(Service, id=service_id)
    if request.method == "POST":
        form = QoutationForm(request.POST, request.FILES)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.service = service
            quote.client = request.user
            quote.save()
            messages.success(request, "Quote was successfully sent to business owners")
            return redirect("listings:get-listing", service.business.slug)
        else:
            return render(request, "markets/quotations/create-quotation.html", {"form": form})
        
    form = QoutationForm
    return render(request, "markets/quotations/create-quotation.html", {"form": form})



