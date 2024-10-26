from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from listings.models import Business
from markets.models import Service, Qoutation
from markets.forms import QoutationForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site

from markets.tasks import send_email_to_owner

@login_required
def get_quotations(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    quotations = Qoutation.objects.filter(service = service)
    return render(request, "markets/quotations/quotations.html", {"quotations": quotations})

@login_required
def quotation_details(request, quotation_id):
    quotation = get_object_or_404(Qoutation, id=quotation_id)
    return render(request, "markets/quotations/quotation.html", {"quotation": quotation})

@login_required
def create_quotation(request, service_id):
    
    service = get_object_or_404(Service, id=service_id)
    form = QoutationForm()
    if request.method == "POST":
        form = QoutationForm(request.POST, request.FILES)
        if form.is_valid():
            quote = form.save(commit=False)
            cd = form.cleaned_data
            quote.service = service
            quote.client = request.user
            quote.save()
            domain = get_current_site(request).domain
            protocol = "https" if request.is_secure() else "http"
            send_email_to_owner(domain, protocol, quote.id)
            messages.success(request, "Quote was successfully sent to business owners")
            return redirect("listings:get-listing", service.business.slug)
        else:
            messages.error(request, "Something is missing, fix error below")
        
    
    return render(request, "markets/quotations/create-quotation.html", {"form": form, "service":service})

@login_required
def delete_quote(request, quotation_id, service_slug):
    service = get_object_or_404(Service, slug=service_slug, business__owner=request.user)
    requested_quotation = get_object_or_404(Qoutation, id = quotation_id, service = service)
    requested_quotation.delete()
    messages.success(request, "Request quotation message deleted")
    return redirect("markets:qoutations")

@login_required
def qoutations(request, service_id = None):
    
    service = None
    quotations = []

    if service_id:
        service = get_object_or_404(Service, id=service_id, organiser=request.user)
        quotations = service.qoutations.all()
    else:
        businesses = Business.objects.prefetch_related("services").filter(owner=request.user)
        quotations = []
        for business in businesses:
            for service in business.services.prefetch_related("qoutations"):
                quotations.extend(service.qoutations.all())

    return render(request, "markets/quotations/manage/quotations.html", {"quotations": quotations, "service": service})
