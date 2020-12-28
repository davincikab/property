from django import forms
from .models import Property, Apartment, Tenants, RentPayment

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ('slug',)

class ApartmentForm(forms.ModelForm):
    
    class Meta:
        model = Apartment
        exclude = ('slug',)

class TenantsForm(forms.ModelForm):
    class Meta:
        model = Tenants
        fields = "__all__"

        # override save 
        # def save(self, )