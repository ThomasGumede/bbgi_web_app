from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from bbgi_home.models import Blog
from listings.models import Business
from campaigns.models import CampaignModel  # Adjust based on your models
from events.models import EventModel  # Adjust based on your models

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return [
            'bbgi_home:bbgi-home',
            'bbgi_home:about-bbgi',
            'bbgi_home:contact',
            'bbgi_home:blogs',
            'campaigns:campaigns',
            'events:events',
            'listings:listings'
        ]

    def location(self, item):
        return reverse(item)


class BusinessSitemap(Sitemap):
    priority = 0.7
    changefreq = 'weekly'

    def items(self):
        return Business.objects.order_by('-created')

    def location(self, obj):
        return reverse('listings:get-listing', args=[obj.slug])

class CampaignSitemap(Sitemap):
    priority = 0.7
    changefreq = 'weekly'

    def items(self):
        return CampaignModel.objects.order_by('-created')

    def location(self, obj):
        return reverse('campaigns:campaign', args=[obj.slug])

class EventSitemap(Sitemap):
    priority = 0.7
    changefreq = 'weekly'

    def items(self):
        return EventModel.objects.order_by('-created')

    def location(self, obj):
        return reverse('events:event-details', args=[obj.slug])
 
class BlogSitemap(Sitemap):
    priority = 0.7
    changefreq = 'weekly'

    def items(self):
        return Blog.objects.order_by('-created')

    def location(self, obj):
        return reverse('bbgi_home:details-blog', args=[obj.slug])
