from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from bbgi_home.forms import MemberForm
from bbgi_home.models import Sponsor, Review
from bbgi_home.utilities.decorators import user_not_superuser_or_staff

@login_required
@user_not_superuser_or_staff
def sponsors(request):
    sponsors = Sponsor.objects.all()
    return render(request, "sponsors/sponsors.html", {"sponsors": sponsors})

def sponsor(request, member_id):
    member = get_object_or_404(Sponsor, id=member_id)
    return render(request, "sponsors/sponsor.html", {"member": member})

@login_required
@user_not_superuser_or_staff
def create_sponsor(request):
    form = MemberForm()
    if request.method == "POST":
        form = MemberForm(data=request.POST, files=request.FILES)
        if form.is_valid() and form.is_multipart():
            form.save()
            messages.success(request, "Sponsor was added successfully!")
            return redirect("bbgi_home:team-members")
        else:
            messages.error(request, "Something went wrong trying to add a sponsor")
            return render(request, "sponsors/create-sponsor.html", {"form": form})
        
    return render(request, "sponsors/create-sponsor.html", {"form": form})

@login_required
@user_not_superuser_or_staff
def update_sponsor(request, sponsor_id):
    sponsor = get_object_or_404(Sponsor, id = sponsor_id)
    form = MemberForm(instance=sponsor)
    if request.method == "POST":
        form = MemberForm(instance=sponsor, data=request.POST, files=request.FILES)
        if form.is_valid() and form.is_multipart():
            form.save()
            messages.success(request, "Sponsor was updated successfully!")
            return redirect("bbgi_home:team-members")
        else:
            messages.error(request, "Something went wrong trying to update a sponsor")
            return render(request, "dashboard/sponsors/create-sponsor.html", {"form": form})
        
    return render(request, "dashboard/sponsors/create-sponsor.html", {"form": form})

@login_required
@user_not_superuser_or_staff
def delete_sponsor(request, sponsor_id):
    sponsor = get_object_or_404(Sponsor, id = sponsor_id)
    sponsor.delete()
    messages.success(request, "sponsor was deleted successfully!")    
    return redirect("bbgi_home:team-sponsors")