from listings.models import Business, BusinessMessages
from listings.forms import BusinessMessageForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

def send_message(request, listing_slug):
    listing = get_object_or_404(Business, slug=listing_slug)
    if request.method == "POST":
        form = BusinessMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.business = listing
            message.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect("listings:get-listing", listing_slug=listing.slug)
        else:
            messages.error(request, "There was an error sending your message. Please try again.")
    else:
        messages.error(request, "Invalid request method.")
        return redirect("listings:get-listing", listing_slug=listing.slug)
    
def get_messages(request, listing_slug):
    listing = get_object_or_404(Business, slug=listing_slug)
    messages = BusinessMessages.objects.filter(listing=listing).order_by("-created_at")
    return render(request, "business/messages/messages.html", {"listing": listing, "messages": messages})