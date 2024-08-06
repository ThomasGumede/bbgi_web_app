from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.contrib import messages
from bbgi_home.forms import EmailForm, SearchForm
from bbgi_home.models import Blog, Member, Privacy
from bbgi_home.tasks import send_email_to_admin
from campaigns.models import CampaignModel
from events.models import EventModel
from listings.models import Business
from markets.models import Service
from django.contrib.auth.decorators import login_required

# Create your views here.
def bbgi_home(request):
    blogs = Blog.objects.all()[:3]
    listings = Business.objects.all()[:4]
    return render(request, "home/home.html", {"posts": blogs, "listings": listings})

def about_bbgi(request):
    members = Member.objects.all()
    return render(request, "home/about-bbgi.html", {"members": members})

def contact(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            form.save()
            send_email_to_admin.delay(form.cleaned_data["subject"], form.cleaned_data["message"], form.cleaned_data["from_email"], form.cleaned_data["name"])
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
def dashboard(request):
    popular_services = Service.objects.filter(is_popular=True, on_discount=True)
    return render(request, "dashboard/dashboard.html", {"popular_services": popular_services})

def search(request):

    form = SearchForm()
    query = request.GET.get("query", None)
    query_by = request.GET.get("search_by", None)
    if not query:
        return render(request, "home/search.html")
    
    results_dic = {
        "campaigns" : CampaignModel.objects.filter(Q(title__icontains=query)| Q(organiser__first_name__icontains=query)),
        "events": EventModel.objects.filter(Q(title__icontains=query)| Q(organiser__first_name__icontains=query)),
        "news": Blog.objects.filter(Q(title__icontains=query)),
        "listings": Business.objects.filter(Q(title__icontains=query)),
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

def terms_and_conditions(request, terms_slug=None):
    legals = Privacy.objects.all().only("slug", "title")
    if terms_slug:
        term = get_object_or_404(Privacy, slug=terms_slug)
    else:
        term = get_object_or_404(Privacy, slug="website-terms-and-community-guidlines")

    return render(request, "home/terms_and_conditions.html", {"legals": legals, "term": term})