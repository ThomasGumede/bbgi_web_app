import json, logging
from django.db.models import Q
from django.forms import formset_factory, modelformset_factory, BaseModelFormSet
from listings.forms import BusinessForm, BusinessSocialForm, BusinessContent, BusinessReviewForm, BusinessUpdateForm, BusinessMessageForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from listings.models import Business, BusinessLocation, Category, BBBEE_RATINGS, BusinessAnalytics
from django.core import serializers
from django.http import JsonResponse
from listings.tasks import send_on_boarding_email
from django.contrib import messages
from django.utils import timezone
from listings.tasks import update_business_analytics

from listings.utilities.custom_methods import sort_listing

def popular_listing_tags(request):
    
    pass

@login_required
def manage_listings(request):
    listings = Business.objects.filter(owner = request.user)
    query = request.GET.get("query", None)

    if query:
        listings = listings.filter(Q(title__icontains=query)| Q(owner__first_name__icontains=query))
        
    return render(request, "business/listing/manage/manage-listings.html", {"listings": listings})

@login_required
def manage_listing(request, listing_slug):
    queryset = Business.objects.all().select_related("category").prefetch_related("business_hours", "reviews", "images")
    listing = get_object_or_404(queryset, slug=listing_slug, owner=request.user)
    try:
        analytics, created = BusinessAnalytics.objects.get_or_create(business=listing, date=timezone.now().date())
        if created:
            pass
        
    except Exception as ex:
        analytics = None
    return render(request, "business/listing/manage/manage-listing.html", {"listing": listing, "analytics": analytics})

def get_started_with_listing(request):
    return render(request, "business/get-started.html")

def get_listings(request, category=None, tag=None):
    query = request.GET.get("search", None)
    category_filter = request.GET.get("category", None)
    sort_by = request.GET.get("sort_by", None)
    province = request.GET.get("province", None)
    bbee_level = request.GET.get("bbbee_level", None)
    
    listings = sort_listing(sort_by, province, bbee_level, query, category_filter, category, tag)
    
    BBEEE = {
        "BEL1": "BBEEE Level 1",
        "BEL2": "BBEEE Level 2",
        "BEL3": "BBEEE Level 3",
        "BEL4": "BBEEE Level 4",
        "BEL5": "BBEEE Level 5",
        "BEL6": "BBEEE Level 6",
        "BEL7": "BBEEE Level 7",
        "NOT": "Not Sure",
        "NC": "Non-compliance",
    }
    context = {
        "listings": listings,
        "query": query, 
        "category_filter": category_filter, 
        "sort_by": sort_by,
        "province": province,
        "bbee_level": bbee_level, "category": category, "tag": tag, "bbee_levels": BBEEE,}

    if tag:
        return render(request, "business/listing/get-listings-by-tag.html", context)

    else:
        return render(request, "business/listing/get-listings.html", context)

def get_listing(request, listing_slug):
    queryset = Business.objects.all().select_related("category").prefetch_related("business_hours", "reviews", "images")
    listing = get_object_or_404(queryset, slug=listing_slug)
    locations = BusinessLocation.objects.filter(business=listing).values("address", "map_coordinates")
    data = json.dumps(list(locations))
    categories = Category.objects.all()
    form = BusinessReviewForm()
    message_form = BusinessMessageForm()
    
    if request.method == "POST":
        form = BusinessReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.business = listing
            if request.user.is_authenticated:
                review.commenter = request.user
            review.save()
            messages.success(request, "Review added successfully")
            return redirect("listings:get-listing", listing_slug=listing.slug)
        else:
        
            messages.error(request, "Error trying to add your review")

    try:
        update_business_analytics.delay(listing.id)
    except Exception as ex:
        logging.error(ex)
        pass
    # update_business_analytics.delay(listing.id)
    return render(request, "business/listing/listing-details.html", {"listing": listing, "form": form, "lcategories": categories, "locations": data, "message_form": message_form})

@login_required
def add_listing(request, listing_slug=None):
    
    
    if listing_slug:
        listing = get_object_or_404(Business, slug=listing_slug, owner=request.user)
        buniness_form = BusinessForm(instance=listing)
        
        if request.method == "POST":
            form = BusinessForm(instance=listing, data=request.POST, files=request.FILES)

            if form.is_valid() and form.is_multipart():
                form.save()
                
                messages.success(request, "Listing created successfully")
                return redirect("listings:add-business-main-location", listing_slug=listing.slug)
            else:
                messages.error(request, "Something went wrong while trying to add your business")
                return render(request, "business/create-listing/add-listing.html", {"listing": listing, "form": form})
        
        return render(request, "business/create-listing/add-listing.html", {"listing": listing, "form": buniness_form})
    
    else:
        
        buniness_form = BusinessForm()
        
        if request.method == "POST":
            form = BusinessForm(request.POST, request.FILES)

            if form.is_valid() and form.is_multipart():
                
                business = form.save(commit=False)
                business.owner = request.user
                business.save()
                
                messages.success(request, "Listing created successfully")
                return redirect("listings:add-business-main-location", listing_slug=business.slug)
            else:
                messages.error(request, "Something went wrong while trying to add your business")
                return render(request, "business/create-listing/add-listing.html", {"form": form})
        
        return render(request, "business/create-listing/add-listing.html", {"form": buniness_form})

@login_required
def add_listing_socials(request, listing_slug):
    listing = get_object_or_404(Business, slug=listing_slug, owner=request.user)
    buniness_form = BusinessSocialForm(instance=listing)
    
    if request.method == "POST":
        form = BusinessSocialForm(instance=listing, data=request.POST)

        if form.is_valid():
            form.save()
            
            
            send_on_boarding_email.delay(listing.id)
            messages.success(request, "Listing created successfully")
            return redirect("markets:add-service", listing_slug=listing.slug)
        else:
            messages.error(request, "Something went wrong while trying to add your business")
            return render(request, "business/create-listing/add-social.html", {"listing": listing, "form": form})
    
    return render(request, "business/create-listing/add-social.html", {"listing": listing, "form": buniness_form})

@login_required
def update_listing_socials(request, listing_slug):
    listing = get_object_or_404(Business, slug=listing_slug, owner=request.user)
    buniness_form = BusinessSocialForm(instance=listing)
    
    if request.method == "POST":
        form = BusinessSocialForm(instance=listing, data=request.POST)

        if form.is_valid():
            form.save()
            
            # send_html_email('New Listing Added', 'listings@bbgi.co.za', 'emails/listing-confirmation.html', {"listing": listing})
            messages.success(request, "Listing contact details updated successfully")
            return redirect("listings:update-listing-socials", listing_slug=listing.slug)
        else:
            messages.error(request, "Something went wrong while trying to update your business")
            return render(request, "business/listing/update/update-listing-social.html", {"listing": listing, "form": form})
    
    return render(request, "business/listing/update/update-listing-social.html", {"listing": listing, "form": buniness_form})


@login_required
def update_listing(request, listing_slug):
    queryset = Business.objects.all().select_related("category").prefetch_related("business_hours", "reviews", "images")
    listing = get_object_or_404(queryset, slug=listing_slug, owner=request.user)
    buniness_form = BusinessUpdateForm(instance=listing)
    

    if request.method == "POST":
        form = BusinessUpdateForm(instance=listing, data=request.POST, files=request.FILES)
        
        if form.is_valid() and form.is_multipart():
            form.save()
            messages.success(request, "Listing updated successfully")
            return redirect("listings:update-listing", listing.slug)
        else:
            messages.error(request, "Something went wrong while trying to update your business")
            return render(request, "business/listing/update-listing.html", {"listing": listing, "form": form})
    else:   
        return render(request, "business/listing/update-listing.html", {"listing": listing, "form": buniness_form})

@login_required
def update_listing_content(request, listing_slug):
    queryset = Business.objects.all().prefetch_related("business_hours")
    listing = get_object_or_404(queryset, slug=listing_slug, owner=request.user)
    
    if request.method == "POST":
        files = request.FILES.getlist("files")
        if len(files) > 0:
            for file in files:
                    business_content = BusinessContent(image=file, business=listing)
                    business_content.save()
            messages.success(request, "Business images added successfully")
            return redirect("listings:update-listing-content", listing.slug)
        else:
            messages.error(request, "Please select atleast one image before submiting form")
            return render(request, "business/listing/update-listing-content.html", {"listing": listing})
    return render(request, "business/listing/update-listing-content.html", {"listing": listing})

@login_required
def delete_listing_content(request, listing_slug, content_id):
    
    listing = get_object_or_404(Business, slug=listing_slug, owner=request.user)
    content = get_object_or_404(BusinessContent, id=content_id, business=listing)
    content.delete()
    messages.success(request, "Image removed successfully")
    return redirect("listings:update-listing-content", listing.slug)

@login_required
def delete_listing(request, listing_slug):
    listing = get_object_or_404(Business, slug=listing_slug, owner=request.user)
    if request.method == "POST":
        listing.delete()
        messages.success(request, "Listing was deleted successfully")
        return redirect("listings:manage-listings")
    else:
        return render(request, "business/listing/delete-listing.html", {"message": f"Are you sure you want to delete this listing ({listing.title})?", "title": "Delete listing", "listing": listing})

@login_required
def get_business_hours_api(request, listing_id):
    try:
        listing = Business.objects.prefetch_related("business_hours").get(id = listing_id)
        business_hours = serializers.serialize("json", listing.business_hours.all())
        return JsonResponse({"success": True, "hours": business_hours}, status=200)
    
    except Business.DoesNotExist:
        return JsonResponse({"success": False, "hours": "Listing does not exists"}, status=200)