from django.db.models import Q
from django.forms import formset_factory, modelformset_factory, BaseModelFormSet
from listings.forms import BusinessForm, BusinessHourForm, BusinessContent, BusinessReviewForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from listings.models import Business, Category, BusinessHour
from django.core import serializers
from django.http import JsonResponse
from markets.forms import ServiceForm, QoutationForm
from django.contrib import messages

from listings.utilities.custom_methods import sort_listing

class BaseBusinessHourFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        self.business = kwargs.pop('business', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instances = super().save(commit=False)
        for instance in instances:
            hour = None
            try:
                hour = self.queryset.get(day=instance.day)
                if self.listings:
                    hour.business = self.business
                    hour.open_time = instance.open_time
                    hour.close_time = instance.close_time
                    hour.operating = instance.operating

                if commit:
                    hour.save()
            except Exception:
                pass
            
            
        self.save_m2m()
        return instances

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
    return render(request, "business/listing/get_listing.html", {"listing": listing})

def get_listings(request, category=None):
    query = request.GET.get("query", None)
    place = request.GET.get("place", None)
    sort_by = request.GET.get("sort_by", None)
    province = request.GET.get("province", None)
    bbee_level = request.GET.get("bbee", None)
    
    listings = sort_listing(sort_by, province, bbee_level, query, place, category)
    
    
    context = {
        "listings": listings,
        "query": query, 
        "place": place, 
        "sort_by": sort_by,
        "province": province,
        "bbee_level": bbee_level, "category": category}
    return render(request, "business/listing/get-listings.html", context)

def get_listing(request, listing_slug):
    queryset = Business.objects.all().select_related("category").prefetch_related("business_hours", "reviews", "images")
    listing = get_object_or_404(queryset, slug=listing_slug)
    categories = Category.objects.all()
    form = BusinessReviewForm()
    form2 = QoutationForm()
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
        
        messages.error(request, "Error trying to add your review")
        return render(request, "business/listing/get-listing.html", {"listing": listing, "form": form})

    return render(request, "business/listing/get-listing.html", {"listing": listing, "form": form, "lcategories": categories, "form2": form2})

@login_required
def add_listing(request):
    if request.user.subscription == None:
        messages.warning(request, "Sorry, you cannot add listing without subscription")
        return redirect("accounts:choose-package")
    
    buniness_form = BusinessForm()
    business_hour_forms = formset_factory(BusinessHourForm, extra=7, max_num=7)
    
    if request.method == "POST":
        form = BusinessForm(request.POST, request.FILES)
        forms = business_hour_forms(request.POST)
        if form.is_valid() and form.is_multipart() and forms.is_valid():
            
            business = form.save(commit=False)
            business.owner = request.user
            business.save()

            for hours in forms:
                business_hours = hours.save(commit=False)
                business_hours.business = business
                business_hours.save()
            
            messages.success(request, "Listing created successfully")
            return redirect("listings:update-listing-content", listing_id=business.id)
        else:
            messages.error(request, "Something went wrong while trying to add your business")
            
            return render(request, "business/listing/add-listing.html", {"form": form, "forms": forms})
    
    return render(request, "business/listing/add-listing.html", {"form": buniness_form, "forms": business_hour_forms})

@login_required
def update_listing(request, listing_slug):
    queryset = Business.objects.all().select_related("category").prefetch_related("business_hours", "reviews", "images")
    listing = get_object_or_404(queryset, slug=listing_slug, owner=request.user)
    buniness_form = BusinessForm(instance=listing)
    

    if request.method == "POST":
        form = BusinessForm(instance=listing, data=request.POST, files=request.FILES)
        
        if form.is_valid() and form.is_multipart():
            form.save()
            messages.success(request, "Listing updated successfully")
            return redirect("listings:manage-listings")
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
        return render(request, "business/listing/delete-listing.html", {"message": f"Are you sure you want to delete this listing ({listing.title})?", "title": "Delete listing"})

@login_required
def get_business_hours_api(request, listing_id):
    try:
        listing = Business.objects.prefetch_related("business_hours").get(id = listing_id)
        business_hours = serializers.serialize("json", listing.business_hours.all())
        return JsonResponse({"success": True, "hours": business_hours}, status=200)
    
    except Business.DoesNotExist:
        return JsonResponse({"success": False, "hours": "Listing does not exists"}, status=200)