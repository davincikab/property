from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.serializers import serialize
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView

# 3rd party imports

# local import
from .models import Property, PropertyImage, Apartment, RentPayment, Tenants
from .forms import PropertyForm, ApartmentForm


def home(request):
    return render(request, 'property/index.html', {'section':'home'})

def filter_property(request):
    if request.GET.get('query'):
        query = request.GET.get('query')
        houses = Property.objects.prefetch_related("property").filter(title__icontains= query)
    else:
        houses = Property.objects.prefetch_related("property").all()
    
    paginator = Paginator(houses, 20)
    page = request.GET.get('page')
    houses = paginator.get_page(page)

    # paginator object
    return render(request, "property/property_list.html", {'houses': houses})

def detail_view(request, title):
    property = get_object_or_404(Property, slug=title)
    house = Property.objects.prefetch_related("property").filter(slug=title)
    print(house[0].property.all())

    # print(house)
    # print(serialize('json', house))
    context = {
        'section':'home', 
        'property':property,
        'images':house[0].property.all()
    }

    return render(request, 'property/property_detail.html', context)

def get_property(request):
    property_data = serialize('geojson', Property.objects.all())
    return HttpResponse(property_data)

def create_property(request):
    if request.method == "POST":
        print(request.POST)

        form = PropertyForm(data=request.POST)
        if form.is_valid():
            house_form = form.save(commit=False)

            # slug
            slug = slugify(house_form.title + str(house_form.pk))
            house_form.slug
            house_form.save()

            # images
            files = request.FILES.getlist('images')
            for image_file in files:
                image = PropertyImage(house=house_form, image=image_file)
                image.save()

            
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
            # get the files 
            files = request.FILES.getlist('images')
            for image_file in files:
                image = PropertyImage(house=house, image=image_file)
                image.save()

            return redirect('/detail/'+ house.slug)
    else:
        form = PropertyForm(instance=house)

    return render(request, 'property/create_property.html',{'section':'Update Property', 'form':form})

def delete_property(request, title):
    house = get_object_or_404(Property, slug=title)

    if request.method == "POST":
        house.delete()
        print('Deleted object')

        return redirect("home")
    return render(request, 'property/delete_property.html',{'section':'Delete Property', 'property':house})


# Apartments 
def list_apartment(request):
    apartment = Apartment.objects.all()
    context = {
        'section':'apartments',
        'apartments':apartment
    }
    return render(request, "property/apartment/apartments_list.html", context)

def filter_apartment(request):
    if request.GET.get('query'):
        query = request.GET.get('query')
        apartments = Apartment.objects.filter(name__icontains=query)
    else:
        apartments = Apartment.objects.all()
    
    # pagination
    paginator = Paginator(apartments, 4)
    page = request.GET.get('page')
    apartments = paginator.get_page(page)

    return render(request, "property/apartment/apartments.html", {"apartments":apartments})

def apartment_data(request):
    apartment = serialize('geojson', Apartment.objects.all())
    return HttpResponse(apartment)


class ApartmentDetailView(DetailView):
    model = Apartment
    template_name = "property/apartment/apartments_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        apartment = kwargs['object']

        context["properties"] = Property.objects.filter(apartment=apartment) 
        context['tenants'] = Tenants.objects.filter(apartment=apartment)

        print(context)
        return context 

# crud list
def create_apartment(request):
    if request.method == "POST":
        form = ApartmentForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect(f"/apartments/")
    else:
        form = ApartmentForm()
    
    return render(request, "property/apartment/apartments_create_update.html",{'form':form})

def update_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    if request.method == "POST":
        form = ApartmentForm(instance=apartment, data=request.POST, files=request.FILES)

        if form.is_valid:
            form.save()

            return redirect(f"/apartments/{apartment.pk}")
    else:
        form = ApartmentForm(instance=apartment)
    
    return render(request, "property/apartment/apartments_create_update.html",{'form':form})

def delete(request):
    pass

# Tenants
def list_tenants(request):
    tenants = Tenants.objects.all()

    context = {
        'section':'tenants',
        'tenants':tenants
    }

    return render(request, "property/tenants/tenants_list.html", context)

# RentPayments
def list_rentpayment(request):
    return render(request, "property/rentpayment_list.html")