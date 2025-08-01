from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.contrib import messages
from bbgi_home.forms import EmailForm, SearchForm
from bbgi_home.models import Blog, Member, Sponsor, Review
from bbgi_home.tasks import send_email_to_admin
from bbgi_home.utilities.decorators import user_not_superuser_or_staff
from bbgi_home.utilities.google_recaptcha import validate_recaptcha
from campaigns.models import CampaignModel
from events.models import EventModel, TicketModel
from listings.models import Business
from markets.models import Service
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger("tasks")
# Create your views here.
def bbgi_home(request):
    blogs = Blog.objects.all()[:5]
    listings = Business.objects.all()[:5]
    events = Business.objects.all()[:5]
    popular_services = Service.objects.filter(is_popular=True, on_discount=True)[:3]
    return render(request, "home/home_v2.html", {"posts": blogs, "listings": listings, "popular_services": popular_services, "events": events})

def about_bbgi(request):
    members = Member.objects.all()
    return render(request, "home/about-bbgi.html", {"members": members})

def contact(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            recaptcha_token = form.cleaned_data.get('recaptcha_token')
            try:
                validate_recaptcha(
                    token=recaptcha_token,
                    project_id=settings.RECAPTCHA_ENTERPRISE_PROJECT_ID,
                    site_key=settings.RECAPTCHA_ENTERPRISE_SITE_KEY,
                )
                form.save()
                send_email_to_admin(form.cleaned_data["subject"], form.cleaned_data["message"], form.cleaned_data["from_email"], form.cleaned_data["name"])
                messages.success(request, "We have successfully receive your email, will be in touch shortly")
                return redirect("bbgi_home:contact")
            
            except ValueError as e:
                logger.error(f"Failed to verify this due to f{e}")
                messages.success(request, "We have successfully receive your email, will be in touch shortly")
                return redirect("bbgi_home:contact")
        else:
            messages.error(request, "Something went wrong, please fix errors below")
            for err in form.errors:
                messages.error(request, f"{err}")
                return render(request, "home/contact.html", {"form": form})
            
    form = EmailForm()
    return render(request, "home/contact.html", {"form": form})

@login_required
@user_not_superuser_or_staff
def dashboard(request):
    events = EventModel.objects.all()
    campaigns = CampaignModel.objects.all()
    listings = Business.objects.all()
    # popular_services = Service.objects.filter(is_popular=True, on_discount=True)
    users = get_user_model().objects.all()
    tickets = TicketModel.objects.count()
    return render(request, "dashboard/dashboard.html", {"listings": listings, "events": events, "campaigns": campaigns, "tickets": tickets, "users": users})

def search(request):

    form = SearchForm()
    query = request.GET.get("query", None)
    query_by = request.GET.get("search_by", None)
    place = request.GET.get("place", None)
    if not query:
        return render(request, "home/search.html")
    
    results_dic = {
        "campaigns" : CampaignModel.objects.filter(Q(title__icontains=query)| Q(organiser__first_name__icontains=query)),
        "events": EventModel.objects.filter(Q(title__icontains=query)| Q(organiser__first_name__icontains=query) | Q(event_address__icontains=place or query)),
        "news": Blog.objects.filter(Q(title__icontains=query)),
        "listings": Business.objects.filter(Q(title__icontains=query) | Q(main_address__icontains=place or query) | Q(bbbee_level__icontains=query)),
    }
    context = {}
    if query and query_by:
        context["results"] = results_dic[query_by]
        context["results_type"] = query_by
        context["query"] = query
    elif query:
        if results_dic["campaigns"].count() > 0:
            context["results"] = results_dic["campaigns"]
            context["results_type"] = "campaigns"
            context["query"] = query
        elif results_dic["events"].count() > 0:
            context["results"] = results_dic["events"]
            context["results_type"] = "events"
            context["query"] = query
        elif results_dic["news"].count() > 0:
            context["results"] = results_dic["news"]
            context["results_type"] = "news"
            context["query"] = query
        else:
            context["results"] = results_dic["listings"]
            context["results_type"] = "listings"
            context["query"] = query
        
        
    
    context["form"] = form
    
    return render(request, "home/search.html", context=context)

def terms_and_conditions(request):
    return render(request, "home/terms_and_conditions.html")

def privacy(request):
    return render(request, "home/privacy.html")

def refunds(request):
    return render(request, "home/refunds.html")

def faqs(request):
    blogs = Blog.objects.all()[:5]
    return render(request, "home/faqs.html", {"posts": blogs})