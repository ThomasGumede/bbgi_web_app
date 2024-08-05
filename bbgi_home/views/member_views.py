from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from bbgi_home.forms import MemberForm
from bbgi_home.models import Member
from bbgi_home.utilities.decorators import user_not_superuser_or_staff

@login_required
@user_not_superuser_or_staff
def team_members(request):
    members = Member.objects.all()
    return render(request, "dashboard/members/members.html", {"members": members})

@login_required
@user_not_superuser_or_staff
def create_member(request):
    form = MemberForm()
    if request.method == "POST":
        form = MemberForm(data=request.POST, files=request.FILES)
        if form.is_valid() and form.is_multipart():
            form.save()
            messages.success(request, "Blog post was created successfully!")
            return redirect("bbgi_home:team-members")
        else:
            messages.error(request, "Something went wrong trying to add a member")
            return render(request, "dashboard/members/create-member.html", {"form": form})
        
    return render(request, "dashboard/members/create-member.html", {"form": form})
