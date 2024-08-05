from markets.models import Service, Qoutation
from django import forms

class QoutationForm(forms.ModelForm):
    class Meta:
        model = Qoutation
        fields = ("full_names", "phone", "email", "file", "description", "location", "call_at", "time")

        widgets = {
            'full_names': forms.TextInput(attrs={"class": "block p-3 md:text-base w-full text-sm text-custom-h outline-none placeholder:text-gray-400 bg-gray-50 rounded-lg border border-gray-300 focus:ring-custom-primary focus:border-custom-primary ease-linear transition-all duration-150"}),
            'file': forms.FileInput(attrs={"class": "w-[0.1px] h-[0.1px] opacity-0 overflow-hidden absolute -z-[1]"}),
            # 'description': forms.TextInput(attrs={"class": "block p-3 md:text-base w-full text-sm text-custom-h outline-none placeholder:text-gray-400 bg-gray-50 rounded-lg border border-gray-300 focus:ring-custom-primary focus:border-custom-primary ease-linear transition-all duration-150"}),
            'email': forms.EmailInput(attrs={"class": "block p-3 md:text-base w-full text-sm text-gray-900 outline-none bg-gray-50 rounded-lg border border-gray-300 focus:ring-custom-primary placeholder:text-gray-400 focus:border-custom-primary ease-linear transition-all duration-150"}),
            'time': forms.Select(attrs={"class": "block p-3 md:text-base w-full text-sm text-custom-h outline-none placeholder:text-gray-400 bg-gray-50 rounded-lg border border-gray-300 focus:ring-custom-primary focus:border-custom-primary ease-linear transition-all duration-150"}),
            'call_at': forms.Select(attrs={"class": "block p-3 md:text-base w-full text-sm text-custom-h outline-none placeholder:text-gray-400 bg-gray-50 rounded-lg border border-gray-300 focus:ring-custom-primary focus:border-custom-primary ease-linear transition-all duration-150"}),
            
            'description': forms.Textarea(attrs={"class": "block p-3 md:text-base w-full text-sm text-custom-h outline-none placeholder:text-gray-400 bg-gray-50 rounded-lg border border-gray-300 focus:ring-custom-primary focus:border-custom-primary ease-linear transition-all duration-150", "rows": 8}),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ("image", "title", "description", "price_decription", "price")

        widgets = {
            'title': forms.TextInput(attrs={"class": "block p-3 md:text-base w-full text-sm text-custom-h outline-none placeholder:text-gray-400 bg-gray-50 rounded-lg border border-gray-300 focus:ring-custom-primary focus:border-custom-primary ease-linear transition-all duration-150"}),
            'image': forms.FileInput(attrs={"class": "w-[0.1px] h-[0.1px] opacity-0 overflow-hidden absolute -z-[1]"}),
            'price_decription': forms.TextInput(attrs={"class": "block p-3 md:text-base w-full text-sm text-custom-h outline-none placeholder:text-gray-400 bg-gray-50 rounded-lg border border-gray-300 focus:ring-custom-primary focus:border-custom-primary ease-linear transition-all duration-150"}),
            'price': forms.NumberInput(
                attrs={
                    'type': 'number',
                    'step': '0.01',
                    'class': 'block p-3 md:text-base w-full text-sm text-custom-h outline-none placeholder:text-gray-400 bg-gray-50 rounded-lg border border-gray-300 focus:ring-custom-primary focus:border-custom-primary ease-linear transition-all duration-150'
                    }
                ),
            'description': forms.Textarea(attrs={"class": "block p-3 md:text-base w-full text-sm text-custom-h outline-none placeholder:text-gray-400 bg-gray-50 rounded-lg border border-gray-300 focus:ring-custom-primary focus:border-custom-primary ease-linear transition-all duration-150", "rows": 8}),
        }