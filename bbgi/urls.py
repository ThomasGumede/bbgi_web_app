from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("bbgi_home.urls", namespace="bbgi_home")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("", include("listings.urls", namespace="listings")),
    path("", include("campaigns.urls", namespace="campaigns")),
    path("", include("events.urls", namespace="events")),
    path("markets/", include("markets.urls", namespace="markets")),
    path("payments/", include("payments.urls", namespace="payments")),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
