from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.serializers import serialize
from django.utils.text import slugify

# 3rd party imports

# local import
from .models import Property
from .forms import PropertyForm


def home(request):
    return render(request, 'property/index.html', {'section':'home'})

def detail_view(request, title):
    property = get_object_or_404(Property, slug=title)
    return render(request, 'property/property_detail.html', {'section':'home', 'property':property})

def get_property(request):
    property_data = serialize('geojson', Property.objects.all())
    return HttpResponse(property_data)

def create_property(request):
    if request.method == "POST":
        print(request.POST)

        form = PropertyForm(data=request.POST)
        if form.is_valid():
            form.save()
            print("Creating")
            slug = slugify(form.cleaned_data['title'])
            return redirect('/detail/'+ slug)
    else:
        form = PropertyForm()
    return render(request, 'property/create_property.html',{'section':'Create Property', 'form':form})

def update_property(request, title):
    house = get_object_or_404(Property, slug=title)
    if request.method == "POST":
        print(request.POST)

        form = PropertyForm(instance=house, data=request.POST)
        if form.is_valid():
            form.save()
            print("Saving")
            return redirect('/detail/'+ house.slug)
    else:
        form = PropertyForm(instance=house)

    return render(request, 'property/create_property.html',{'section':'Update Property', 'form':form})

def delete_property(request):
    return render(request, 'property/delete_property.html',{'section':'Create Property'})

