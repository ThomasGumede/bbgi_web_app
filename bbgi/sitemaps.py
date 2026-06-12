from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from bbgi_home.models import Blog
from listings.models import Business, Category
from campaigns.models import CampaignModel
from events.models import EventModel
from taggit.models import Tag


PROVINCES = [
    ("KZN", "KwaZulu-Natal"),
    ("MP", "Mpumalanga"),
    ("NW", "North-West"),
    ("FS", "Free-State"),
    ("WC", "Western Cape"),
    ("LP", "Limpopo"),
    ("GP", "Gauteng"),
    ("EC", "Eastern Cape"),
    ("NC", "Northern Cape"),
]


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = "daily"

    def items(self):
        return [
            "bbgi_home:bbgi-home",
            "bbgi_home:about-bbgi",
            "bbgi_home:contact",
            "bbgi_home:blogs",
            "campaigns:campaigns",
            "events:events",
            "listings:listings",
        ]

    def location(self, item):
        return reverse(item)


class ProvinceSitemap(Sitemap):
    priority = 0.8
    changefreq = "daily"

    def items(self):
        return [code for code, _ in PROVINCES]

    def location(self, obj):
        return reverse(
            "listings:get-listings-by-province",
            kwargs={"province": obj}
        )


class CategorySitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return getattr(obj, "updated", None)

    def location(self, obj):
        return reverse(
            "listings:get-listings-by-category",
            kwargs={"category": obj.slug}
        )


class TagSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return Tag.objects.all()

    def location(self, obj):
        return reverse(
            "listings:get-listings-by-tag",
            kwargs={"tag": obj.slug}
        )


class BusinessSitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return Business.objects.filter(
            is_completed=True
        ).order_by("-created")

    def lastmod(self, obj):
        return getattr(obj, "updated", obj.created)

    def location(self, obj):
        return reverse(
            "listings:get-listing",
            kwargs={"listing_slug": obj.slug}
        )


class CampaignSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return CampaignModel.objects.order_by("-created")

    def lastmod(self, obj):
        return getattr(obj, "updated", obj.created)

    def location(self, obj):
        return reverse(
            "campaigns:campaign",
            kwargs={"campaign_slug": obj.slug}
        )


class EventSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return EventModel.objects.order_by("-created")

    def lastmod(self, obj):
        return getattr(obj, "updated", obj.created)

    def location(self, obj):
        return reverse(
            "events:event-details",
            kwargs={"event_slug": obj.slug}
        )


class BlogSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return Blog.objects.order_by("-created")

    def lastmod(self, obj):
        return getattr(obj, "updated", obj.created)

    def location(self, obj):
        return reverse(
            "bbgi_home:details-blog",
            kwargs={"post_slug": obj.slug}
        )


sitemaps = {
    "static": StaticViewSitemap,
    "provinces": ProvinceSitemap,
    "categories": CategorySitemap,
    "tags": TagSitemap,
    "businesses": BusinessSitemap,
    "campaigns": CampaignSitemap,
    "events": EventSitemap,
    "blogs": BlogSitemap,
}
