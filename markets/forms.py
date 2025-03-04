from markets.models import RequestService, Service, Qoutation
from django import forms

class QoutationForm(forms.ModelForm):
    class Meta:
        model = Qoutation
        fields = ("full_names", "phone", "email", "file", "description", "location", "call_at", "time")

        widgets = {
            'full_names': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'file': forms.FileInput(attrs={"class": "w-[0.1px] h-[0.1px] opacity-0 overflow-hidden absolute -z-[1]"}),
            'location': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'email': forms.EmailInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'time': forms.Select(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'call_at': forms.Select(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            
            'description': forms.Textarea(attrs={"class": "!min-h-[50px] text-custom-text pl-5 pr-[50px] py-[15px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "rows": 8, "placeholder": "Problem Description"}),
        }

class RequestServiceForm(forms.ModelForm):
    class Meta:
        model = RequestService
        fields = ("full_names", "phone", "email", "file", "description", "location", "call_at", "time", "service_title")

        widgets = {
            'full_names': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'file': forms.FileInput(attrs={"class": "w-[0.1px] h-[0.1px] opacity-0 overflow-hidden absolute -z-[1]"}),
            'location': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'email': forms.EmailInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'time': forms.Select(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'call_at': forms.Select(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'service_title': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'description': forms.Textarea(attrs={"class": "!min-h-[50px] text-custom-text pl-5 pr-[50px] py-[15px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "rows": 8, "placeholder": "Problem Description"}),
        }

class ServiceForm(forms.ModelForm):
    add_another = forms.CharField(max_length=100, required=False)
    class Meta:
        model = Service
        fields = ("image", "title", "description", "price_decription", "price")

        widgets = {
            'title': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'image': forms.FileInput(attrs={"class": "w-[0.1px] h-[0.1px] opacity-0 overflow-hidden absolute -z-[1]"}),
            'price_decription': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'price': forms.NumberInput(
                attrs={
                    'type': 'number',
                    'step': '0.01',
                    'class': 'text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm'
                    }
                ),
            'description': forms.Textarea(attrs={"class": "!min-h-[50px] text-custom-text pl-5 pr-[50px] py-[15px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "rows": 8, "placeholder": "Service Description"}),
        }