from django import forms

class CouponApplyForm(forms.Form):
    code = forms.CharField()
    return_url = forms.CharField()