from django import forms
from .models import Property, Apartment, Tenants, RentPayment

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ('slug',)

class ApartmentForm(forms.ModelForm):
    
    class Meta:
        model = Apartment
        fields = "__all__"

