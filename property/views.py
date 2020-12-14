from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Property
from django.core.serializers import serialize

# Create your views here.
def home(request):
    return render(request, 'property/index.html', {'section':'home'})

def detail_view(request, title):
    property = get_object_or_404(Property, slug=title)
    return render(request, 'property/property_detail.html', {'section':'home', 'property':property})

def get_property(request):
    property_data = serialize('geojson', Property.objects.all())
    return HttpResponse(property_data)

def create_property(request):
    return render(request, 'property/create_property.html',{'section':'Create Property'})

# 
