from django.utils import timezone

COMPANY = {
    "facebook": "https://www.facebook.com/blackbusinessgrowthinitiave",
    "tiktok": "https://wwww.tiktok.com/@BBGInitiative",
    "instagram": "https://www.instagram.com/blackbusinessgrowthinitiave",
    "linkedIn": "https://www.linkedin.com/company/black-business-growth-initiative/posts/",
    "website": "https://bbgi.co.za",
    "company_support_mail": "info@bbgi.co.za",
    "phone": "021 830 5415",
    "youtube": "https://www.youtube.com/@blackbusinessgrowthinitiat6153",
    "company_street_address_1": "COMPANY.address_one",
    "company_city": "COMPANY.city",
    "company_state": "COMPANY.province",
    "company_zipcode": "zipcode"

}

def generate_order_number(model) -> str:
    order_id_start = f'BBGI{timezone.now().year}{timezone.now().month}'
    queryset = model.objects.filter(order_id__iexact=order_id_start).count()
      
    count = 1
    order_id = order_id_start
    while(queryset):
        order_id = f'BBGI{timezone.now().year}{timezone.now().month}{count}'
        count += 1
        queryset = model.objects.all().filter(order_id__iexact=order_id).count()

    return order_id