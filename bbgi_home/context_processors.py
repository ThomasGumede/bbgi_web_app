from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from accounts.utilities.company import COMPANY
from listings.models import Category
from bbgi_home.models import BlogCategory

def global_context(request):
    PROTOCOL = "https" if request.is_secure() else "http"
    DOMAIN = get_current_site(request).domain

    context = {
        'domain' : DOMAIN,
        'protocol': PROTOCOL,
        "blog_categories": BlogCategory.objects.all(),
        "listing_categories": Category.objects.all(),
        "facebook": COMPANY["facebook"],
        "twitter": COMPANY["twitter"],
        "linkedIn": COMPANY["linkedIn"],
        "company_support": COMPANY["phone"],
        "company_support_mail": COMPANY["company_support_mail"], 
        "company_street_address_1": COMPANY["company_street_address_1"],
        "company_city": COMPANY["company_city"],
        "company_state": COMPANY["company_state"],
        "company_zipcode": COMPANY["company_zipcode"],
    }

    

    return context