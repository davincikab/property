from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'property/index.html', {'section':'home'})

def detail_view(request):
     return render(request, 'property/property_detail.html', {'section':'home'})

def create_property(request):
    return render(request, 'property/create_property.html',{'section':'Create Property'})

# 
