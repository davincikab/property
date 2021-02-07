from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import login
from django.views.generic.edit import FormView, CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict

from .forms import LandlordSignUpForm, AgencySignUpForm, ProfileForm
from property.models import Apartment
from .models import User, UserProfile

# Create your views here.
def signup(request):
    return render(request, "account/signup.html")

class LandlordSignUpView(CreateView):
    model = User
    form_class = LandlordSignUpForm
    template_name = "account/register.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kwargs['user_type'] = 'landlord'
        context['title'] = "Landlord Registration"
       
        return context
    
    def form_valid(self, form):
        user = form.save()
        user.is_landlord = True
        user.save()

        login(self.request, user)
        return redirect('home')
        

class AgencySignUpView(CreateView):
    model = User
    form_class = AgencySignUpForm
    template_name = "account/register.html"    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kwargs['user_type'] = 'agency'
        context['title'] = "Agency Registration "

        return context
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.save()
        login(self.request, user)
        return redirect('home')
   

# profile view
class ProfileCreateView(LoginRequiredMixin, FormView):
    login_url = "/user/login/"
    model = UserProfile
    form_class = ProfileForm
    template_name = "account/create_profile.html"
    success_url = "/account/profile"     

    def get_initial(self):  
        user = User.objects.get(username = self.request.user.username)
        try:
            profile = UserProfile.objects.get(user=self.request.user)

            # get plot info 

            profile = {**model_to_dict(profile), **model_to_dict(user)}
        except UserProfile.DoesNotExist:
            profile = model_to_dict(user)
        
        return profile
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def form_valid(self, form):
        profile = form.save(commit=False)

        try:
            user_profile = UserProfile.objects.get(user=self.request.user)
            form = self.form_class(self.request.POST or None, self.request.FILES, instance=user_profile)
            form.save()
        except UserProfile.DoesNotExist:
            print(self.request.FILES)
            profile.user = self.request.user
            # profile.image = self.request.FILES
            profile.save()
            
           

        print('Valid')
        user_details = self.request.user

        from operator import itemgetter
        first_name, last_name, surname = itemgetter('first_name', 'last_name', 'surname')(self.request.POST)

        user_details.first_name = first_name
        user_details.last_name = last_name
        user_details.surname = surname

        user_details.save()

        return redirect(self.success_url)
    
    def form_invalid(self, form):
        print(form)
        print(form.errors)
        return HttpResponse("Invalid data")

class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = '/user/login/' 
    template_name = "account/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            username = self.request.GET.get('user', None)
            # print(User.objects.get(username=user))
            if username:
                context['profile'] = UserProfile.objects.get(user__username=username)
                context['apartments'] = Apartment.objects.filter(agent__user__username=username)
            else:
                context['profile'] = UserProfile.objects.get(user=self.request.user)
                context['apartments'] = Apartment.objects.filter(agent__user=self.request.user)
        except UserProfile.DoesNotExist or User.DoesNotExist:
            print("Failed")
            context["profile"] = {}
            context['apartments'] = {}
        
        return context
    