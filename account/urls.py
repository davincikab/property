from django.urls import path
from .views import LandlordSignUpView, signup, AgencySignUpView

urlpatterns = [
    path("", signup, name="signup"),
    path("signup/agency", AgencySignUpView.as_view(), name="agency-signup"),
    path("signup/landlord", LandlordSignUpView.as_view(), name="landlord-signup"), 
]
