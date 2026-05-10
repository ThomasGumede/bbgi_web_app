from events.models import EventModel
from campaigns.models import CampaignModel
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from listings.models import Business

@login_required
def get_business_events(request, listing_slug):
    listing = get_object_or_404(Business, slug=listing_slug, owner=request.user)
    events = EventModel.objects.filter(company_organiser=listing, organiser=request.user)
    return render(request, 'business/manage/manage_business_events.html', {'events': events, "listing": listing})

@login_required
def get_business_campaigns(request, listing_slug):
    listing = get_object_or_404(Business, slug=listing_slug, owner=request.user)
    campaigns = CampaignModel.objects.filter(company_organiser=listing, organiser=request.user)
    return render(request, 'business/manage/manage_business_campaigns.html', {'campaigns': campaigns, "listing": listing})

