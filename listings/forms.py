from django import forms
from listings.models import Business, BusinessContent, BusinessHour, BusinessLocation, BusinessReview, ListingOrder
from tinymce.widgets import TinyMCE


class ListingOrderForm(forms.ModelForm):
    class Meta:
        model = ListingOrder
        fields = ("client_first_name", "client_last_name", "client_phone", "client_email", "client_address_one", "client_address_two", "client_city", "client_zipcode", "client_province")

        widgets = {
            'client_address_one': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'client_address_two': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'client_city': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'client_country': forms.TextInput(attrs={"value": "South Africa", "class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'client_province': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'client_zipcode': forms.NumberInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"})
        }

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = (
            "title", "background_image", "logo", 
            "details", "slogan", "category", "bbbee_level", 
        )

        widgets = {
            'background_image': forms.FileInput(attrs={"class": "w-[0.1px] h-[0.1px] opacity-0 overflow-hidden absolute -z-[1]"}),
            'logo': forms.FileInput(attrs={"class": "w-[0.1px] h-[0.1px] opacity-0 overflow-hidden absolute -z-[1]"}),
            
            'website': forms.URLInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "e.g https://www.business.co.za"}),
            'slogan': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'email': forms.EmailInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "e.g info@business.co.za"}),
            'category': forms.Select(attrs={"class": "selectize"}),
            'bbbee_level': forms.Select(attrs={"class": "selectize"}),
            'title': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'details': forms.Textarea(attrs={"class": "!min-h-[50px] text-custom-text pl-5 pr-[50px] py-[15px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "rows": 8, "placeholder": "Business Description"}),
            'zipcode': forms.NumberInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"})
            
        }

class BusinessUpdateForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ("title", "background_image", "logo", 
            "details", "slogan", "category", "bbbee_level", "main_address", "map_coordinates", "facebook", "twitter", "instagram", "linkedIn", "phone", "website", "email", "alternative_phone")

        widgets = {
            'background_image': forms.FileInput(attrs={"class": "w-[0.1px] h-[0.1px] opacity-0 overflow-hidden absolute -z-[1]"}),
            'logo': forms.FileInput(attrs={"class": "w-[0.1px] h-[0.1px] opacity-0 overflow-hidden absolute -z-[1]"}),
            'main_address': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'website': forms.URLInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "e.g https://www.business.co.za"}),
            'slogan': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'email': forms.EmailInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "e.g info@business.co.za"}),
            'category': forms.Select(attrs={"class": "selectize"}),
            'bbbee_level': forms.Select(attrs={"class": "selectize"}),
            'title': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'details': forms.Textarea(attrs={"class": "!min-h-[50px] text-custom-text pl-5 pr-[50px] py-[15px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "rows": 8, "placeholder": "Business Description"}),
            'zipcode': forms.NumberInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'map_coordinates': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'address': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'website': forms.URLInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "e.g https://www.business.co.za"}),
            'email': forms.EmailInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "e.g info@business.co.za"}),
            
        }

class BusinessLocationForm(forms.ModelForm):
    class Meta:
        model = BusinessLocation
        fields = ("address", "map_coordinates")

        widgets = {
            'map_coordinates': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'address': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            
        }

class BusinessMainLocationForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ("map_coordinates", "main_address")

        widgets = {
            
            'map_coordinates': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'main_address': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            
        }

class BusinessSocialForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ("facebook", "twitter", "instagram", "linkedIn", "phone", "website", "email", "alternative_phone")

        widgets = {
            
            'website': forms.URLInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "e.g https://www.business.co.za"}),
            'email': forms.EmailInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "e.g info@business.co.za"}),
             
        }

class BusinessHourForm(forms.ModelForm):
    class Meta:
        model = BusinessHour
        exclude=["id"]
        fields = ("day", "open_time", "close_time", "operating")

class BusinessReviewForm(forms.ModelForm):
    class Meta:
        model = BusinessReview
        fields = ("comment", "commenter_full_names", "commenter_email", "rating_value", "comment_title")

        widgets = {
            'rating_value': forms.HiddenInput(),
            'commenter_full_names': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "Type your name..."}),
            'commenter_email': forms.EmailInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "Type your email..."}),
            'comment_title': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "Type your comment title..."}),
            
            'comment': forms.Textarea(attrs={"class": "!min-h-[50px] text-custom-text pl-5 pr-[50px] py-[15px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "rows": 8, "placeholder": "Type your comment..."}),
        }