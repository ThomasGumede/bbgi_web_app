from listings.models import Business, BusinessMessages
from listings.forms import BusinessMessageForm
from listings.utilities.custom_shortcuts import get_listing_or_404
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

@login_required    
def get_messages(request, listing_slug):
    listing = get_object_or_404(Business,  slug=listing_slug, owner=request.user)
    bmessages = BusinessMessages.objects.filter(business=listing).order_by("-created")
    return render(request, "business/messages/messages.html", {"listing": listing, "bmessages": bmessages})

@login_required
def get_message(request, message_id, listing_slug):
    listing = get_object_or_404(Business, slug=listing_slug, owner=request.user)
    try:
        message = BusinessMessages.objects.get(id=message_id, business=listing)
        return render(request, "business/messages/message.html", {"listing": listing, "bmessage": message})
    except BusinessMessages.DoesNotExist as ex:
        return render(request, "business/not-found.html", {"listing": listing})
    
    

@login_required
def delete_message(request, message_id, listing_slug):
    listing = get_object_or_404(Business, slug=listing_slug, owner=request.user)
    message = get_listing_or_404(BusinessMessages, request=request, template='business/not-found.html', context={'listing': listing}, id=message_id, business=listing)
    return render(request, "business/messages/message.html", {"listing": listing, "message": message})