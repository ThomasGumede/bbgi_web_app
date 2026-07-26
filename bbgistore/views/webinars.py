from bbgistore.models.webinar import Webinar
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from bbgistore.models.abstract import StoreCategory

def all_webinars(request, category_slug=None):
    webinars = Webinar.objects.filter(status="published").order_by('-created')
    query = request.GET.get("q", None)
    if category_slug:
        category = get_object_or_404(StoreCategory, slug=category_slug)
        webinars = webinars.filter(category=category)
    
    if query:
        webinars = webinars.filter(title__icontains=query) 
           
    context = {
        "webinars": webinars
    }
    return render(request, "bbgistore/webinars/all-webinars.html", context)

def get_webinar_details(request, webinar_slug):
    webinar = get_object_or_404(Webinar, slug=webinar_slug)
    return render(request, "bbgistore/webinars/webinar-details.html", {"webinar": webinar})