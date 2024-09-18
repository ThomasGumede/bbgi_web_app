from accounts.models import AboutCompany
from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# forms
class CompanyAddressForm(forms.ModelForm):
    class Meta:
        model = AboutCompany
        fields = ("address_one", "city", "province", "address_two", "zipcode", "email", "phone", "linkedIn", "facebook", "twitter", "instagram", "small_description", "slogan", "title")

@login_required
def update_company_address(request):
    company = get_object_or_404(AboutCompany, slug="about-bbgi-model")
    form = CompanyAddressForm(instance=company)
    if request.method == "POST":
        form = CompanyAddressForm(instance=company, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Company details updated successfully")
            return redirect("accounts:update-company-details")
        else:
            messages.error(request, "Please fix errors below")
            return render(request, "accounts/company/update-address.html", {"form": form, "company": company})
    return render(request, "accounts/company/update-address.html", {"form": form, "company": company})
