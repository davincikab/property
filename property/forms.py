from django import forms
from django.core.files.base import ContentFile


import base64

from .models import Property, Apartment, Tenants, RentPayment

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ('slug',)

class ApartmentForm(forms.ModelForm):
    
    class Meta:
        model = Apartment
        exclude = ('slug','agent')

class TenantsForm(forms.ModelForm):
    class Meta:
        model = Tenants
        fields = "__all__"

        # override save 
        # def save(self, )

class RentPaymentForm(forms.ModelForm):
    
    class Meta:
        model = RentPayment
        exclude = ('receipt', )
    
    def save(self, force_insert=False, force_update=False, commit=True, receiptString=""):
        receipt = super().save(commit=False)
        image_data = receiptString

        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]

        data = ContentFile(base64.b64decode(imgstr))  
        file_name = self.cleaned_data['receipt_number'] + "." + ext

        receipt.receipt.save(file_name, data, save=False)

        if commit:
            receipt.save()
        return receipt
        
