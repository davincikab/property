from django.shortcuts import render, redirect
from .forms import LandlordSignUpForm, AgencySignUpForm
from django.views.generic import CreateView
from django.contrib.auth import login
from .models import User

# Create your views here.
def signup(request):
    return render(request, "account/signup.html")
    
class LandlordSignUpView(CreateView):
    model = User
    form_class = LandlordSignUpForm
    template_name = "account/register.html"

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'landlord'
       
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')
        

class AgencySignUpView(CreateView):
    model = User
    form_class = AgencySignUpForm
    template_name = "account/register.html"

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'agency'
       
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')
   



