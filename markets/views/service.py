from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from listings.models import Business
from markets.models import Service
from markets.forms import ServiceForm
from django.contrib import messages


@login_required
def get_services(request, listing_slug):
    listing = get_object_or_404(Business, slug=listing_slug, owner=request.user)
    services = Service.objects.filter(business = listing)
    return render(request, "markets/services/services.html", {"listing": listing, "services": services})

def service_details(request, service_slug):
    service = get_object_or_404(Service, slug=service_slug)
    return render(request, "markets/services/service-details.html", {"service": service})

def all_services(request):
    services = Service.objects.all()
    query = request.GET.get("query", None)
    if query:
        services = Service.objects.filter(Q(title__icontains=query) | Q(business__title__icontains=query))
    return render(request, "markets/services/all-services.html", {"services": services, "query": query})

@login_required
def add_service(request, listing_slug):
    listing = get_object_or_404(Business, slug=listing_slug, owner=request.user)
    form = ServiceForm()

    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid() and form.is_multipart():
            add_another = form.cleaned_data.get("add_another", None)
            title = form.cleaned_data.get("title", None)
            service = form.save(commit=False)
            service.business = listing
            service.save()
            
            if add_another:
                messages.success(request, f"Service ({title}) added successfully")
                return redirect("markets:add-service", listing.slug)
            messages.success(request, f"Your business was added successfully. To verify, please make payment")
            return redirect("listings:order-subscription", listing.slug)
        else:
            messages.error(request, "Error trying to create service")
            
        
    return render(request, "business/create-listing/add-services.html", {"form": form, "listing": listing})

@login_required
def create_service(request, listing_slug):
    listing = get_object_or_404(Business, slug=listing_slug, owner=request.user)
    form = ServiceForm()

    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid() and form.is_multipart():
            service = form.save(commit=False)
            service.business = listing
            service.save()
            messages.success(request, "Service added successfully")
            return redirect("markets:get-services", listing.slug)
        else:
            messages.error(request, "Error trying to create service")
            return render(request, "markets/services/create-service.html", {"form": form})
        
    return render(request, "markets/services/create-service.html", {"form": form, "listing": listing})

@login_required
def update_service(request, listing_slug, service_id):
    listing = get_object_or_404(Business, slug=listing_slug, owner=request.user)
    service = get_object_or_404(Service, id=service_id, business=listing)
    form = ServiceForm(instance=service)

    if request.method == "POST":
        form = ServiceForm(instance=service, data=request.POST, files=request.FILES)
        if form.is_valid() and form.is_multipart():
            service.save()
            messages.success(request, "Service updated successfully")
            return redirect("markets:get-services", listing.slug)
        else:
            messages.error(request, "Error trying to update service")
            return render(request, "markets/services/update-service.html", {"form": form})
        
    return render(request, "markets/services/update-service.html", {"form": form, "listing": listing})

@login_required
def delete_service(request, listing_slug, service_id):
    listing = get_object_or_404(Business, slug=listing_slug, owner=request.user)
    service = get_object_or_404(Service, id=service_id, business=listing)
    if request.method == "POST":
        service.delete()
        messages.success(request, "Service was deleted successfully")
        return redirect("markets:get-services", listing.id)
    return render(request, "markets/services/delete-service.html", {"listing": listing, "service": service})
