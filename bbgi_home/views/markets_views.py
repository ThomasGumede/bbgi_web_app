from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from listings.models import Business
from markets.models import Service, Qoutation
from markets.forms import ServiceForm, QoutationForm
from django.contrib import messages

@login_required
def all_quotations(request):
    quotations = Qoutation.objects.filter(client=request.user)
    return render(request, "dashboard/markets/quotations/quotations.html", {"quotations": quotations})

