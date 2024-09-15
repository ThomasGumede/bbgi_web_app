from accounts.models import AboutCompany
from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

# forms
class CompanyAddressForm(forms.ModelForm):
    class Meta:
        model = AboutCompany
        fields = ("address_one", "city", "province", "address_two", "zipcode")

@login_required
def update_company_address(request):
    company = get_object_or_404(AboutCompany, slug="about-bbgi-model")
