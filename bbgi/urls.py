from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from .sitemaps import StaticViewSitemap, CampaignSitemap, EventSitemap, BlogSitemap, BusinessSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'listings': BusinessSitemap,
    'campaigns': CampaignSitemap,
    'events': EventSitemap,
    'blogs': BlogSitemap
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("bbgi_home.urls", namespace="bbgi_home")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("", include("listings.urls", namespace="listings")),
    path("", include("campaigns.urls", namespace="campaigns")),
    path("", include("events.urls", namespace="events")),
    path("", include("coupons.urls", namespace="coupons")),
    path("", include("markets.urls", namespace="markets")),
    path("payments/", include("payments.urls", namespace="payments")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
