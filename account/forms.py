from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class AgencySignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password", "password2", "first_name", "last_name", "phone_number",)
    
    def save(self):
        user = super().save(commit=False)
        user.is_agency = True
        return user

class LandlordSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password", "password2", "first_name", "last_name", "phone_number",)
    
    def save(self):
        user = super().save(commit=False)
        user.is_landlord = True
        return user
