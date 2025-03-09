from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from bbgi_home.forms import SponsorForm, ReviewForm
from bbgi_home.models import Sponsor, Review
from bbgi_home.utilities.decorators import user_not_superuser_or_staff

@login_required
@user_not_superuser_or_staff
def sponsors(request):
    sponsors = Sponsor.objects.all()
    return render(request, "sponsors/sponsors.html", {"sponsors": sponsors})

def sponsor(request, sponsor_id):
    sponsor = get_object_or_404(Sponsor, id=sponsor_id)
    return render(request, "sponsors/sponsor.html", {"sponsor": sponsor})

@login_required
@user_not_superuser_or_staff
def create_sponsor(request):
    form = SponsorForm()
    if request.method == "POST":
        form = SponsorForm(data=request.POST, files=request.FILES)
        if form.is_valid() and form.is_multipart():
            form.save()
            messages.success(request, "Sponsor was added successfully!")
            return redirect("bbgi_home:sponsors")
        else:
            messages.error(request, "Something went wrong trying to add a sponsor")
            return render(request, "sponsors/create-sponsor.html", {"form": form})
        
    return render(request, "sponsors/create-sponsor.html", {"form": form})

@login_required
@user_not_superuser_or_staff
def update_sponsor(request, sponsor_id):
    sponsor = get_object_or_404(Sponsor, id = sponsor_id)
    form = SponsorForm(instance=sponsor)
    if request.method == "POST":
        form = SponsorForm(instance=sponsor, data=request.POST, files=request.FILES)
        if form.is_valid() and form.is_multipart():
            form.save()
            messages.success(request, "Sponsor was updated successfully!")
            return redirect("bbgi_home:sponsors")
        else:
            messages.error(request, "Something went wrong trying to update a sponsor")
            return render(request, "sponsors/create-sponsor.html", {"form": form})
        
    return render(request, "sponsors/create-sponsor.html", {"form": form})

@login_required
@user_not_superuser_or_staff
def delete_sponsor(request, sponsor_id):
    sponsor = get_object_or_404(Sponsor, id = sponsor_id)
    sponsor.delete()
    messages.success(request, "sponsor was deleted successfully!")    
    return redirect("bbgi_home:sponsors")


@login_required
@user_not_superuser_or_staff
def reviews(request):
    reviews = Review.objects.all()
    return render(request, "reviews/reviews.html", {"reviews": reviews})


@login_required
@user_not_superuser_or_staff
def create_review(request):
    form = ReviewForm()
    if request.method == "POST":
        form = ReviewForm(data=request.POST, files=request.FILES)
        if form.is_valid() and form.is_multipart():
            form.save()
            messages.success(request, "Review was added successfully!")
            return redirect("bbgi_home:reviews")
        else:
            messages.error(request, "Something went wrong trying to add a review")
            return render(request, "reviews/create-review.html", {"form": form})
        
    return render(request, "reviews/create-review.html", {"form": form})

@login_required
@user_not_superuser_or_staff
def update_review(request, review_id):
    review = get_object_or_404(Review, id = review_id)
    form = ReviewForm(instance=review)
    if request.method == "POST":
        form = ReviewForm(instance=review, data=request.POST, files=request.FILES)
        if form.is_valid() and form.is_multipart():
            form.save()
            messages.success(request, "Review was updated successfully!")
            return redirect("bbgi_home:reviews")
        else:
            messages.error(request, "Something went wrong trying to update a sponsor")
            return render(request, "reviews/create-sponsor.html", {"form": form})
        
    return render(request, "reviews/create-sponsor.html", {"form": form})

@login_required
@user_not_superuser_or_staff
def delete_review(request, review_id):
    review = get_object_or_404(Review, id = review_id)
    review.delete()
    messages.success(request, "review was deleted successfully!")    
    return redirect("bbgi_home:reviews")