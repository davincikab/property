from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.serializers import serialize
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.template.loader import get_template

# 3rd party imports
from datetime import datetime
from xhtml2pdf import pisa
from io import BytesIO
import os
import json

# local import
from .models import Property, PropertyImage, Apartment, RentPayment, Tenants
from .forms import PropertyForm, ApartmentForm, TenantsForm, RentPaymentForm


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

def delete_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)

    if request.method == "POST":
        apartment.delete()
        return redirect("/apartments/")
    
    return render(request, "property/apartment/apartments_delete.html", {'apartment':apartment})

# ========================== Tenants
def list_tenants(request):
    tenants = Tenants.objects.all()
    active_tag = ""

    if request.GET.get('query'):
        query = request.GET.get('query')
        tenants = Tenants.objects.filter(first_name__icontains = query)
    
    if request.GET.get('house_type'):
        query = request.GET.get('house_type')
        active_tag = query
        tenants = Tenants.objects.filter(room_type__icontains = query)
    
    paginator = Paginator(tenants, 10)
    page = request.GET.get('page')
    tenants = paginator.get_page(page)

    context = {
        'section':'tenants',
        'tenants':tenants,
        'house_types': ['Single Rooms', 'Bed Sitter', 'One Bedroom', 'Two Bedroom', 'Three Bedroom', 'Four Bedroom', 'Five Bedroom'],
        'active_tag':active_tag
    }

    return render(request, "property/tenants/tenants_list.html", context)

class TenantDetailView(DetailView):
    model = Tenants
    template_name = "property/tenants/tenants_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tenant = kwargs['object']

        context["payments"] = RentPayment.objects.filter(tenant=tenant)
        context['is_rent_paid'] = self.is_rent_paid(tenant)
        return context

    def is_rent_paid(self, tenant):
        current_date = datetime.now()
        payments = RentPayment.objects.filter(tenant=tenant)\
            .filter(paid_on__year=current_date.year) \
            .filter(paid_on__month=current_date.month)
        
        print(payments)
        
        if len(payments) == 1:
            return True
        return False

class TenantsCreateView(CreateView):
    model = Tenants
    template_name = "property/tenants/tenants_create.html"
    form_class = TenantsForm

    extra_context = {
        'section':"Add a Tenant"
    }

    def get(self, request, *args, **kwargs):
        print('form initial')
        print(kwargs['title'])
        title = kwargs['title']
        apartment = Apartment.objects.get(slug=title)

        self.initial = {
            'geom':apartment.geom,
            'apartment':apartment
        }

        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        form.save()
        return redirect("/tenants/")

class TenantsUpdateView(UpdateView):
    model = Tenants
    form_class = TenantsForm
    template_name = "property/tenants/tenants_create.html"
    extra_context = {
        'section':"Update Tenant Info"
    }

    def form_valid(self, form):
        form.save()
        tenant = self.object

        print(tenant)
        url = f"/tenants/{tenant.pk}"
        return redirect(url)
    

class TenantsDeleteView(DeleteView):
    model = Tenants
    template_name = "property/tenants/tenants_delete.html"
    success_url = "/tenants/"
    context_object_name = "tenant"

# ============================== RentPayments
def list_rentpayment(request):
    return render(request, "property/rentpayment_list.html")

# pay rent
def make_payment(request, title, tenant_id):
    tenant = get_object_or_404(Tenants, pk=tenant_id)
    apartment = get_object_or_404(Apartment, slug=title)

    current_date = timezone.now()
    context = {
        'tenant':tenant, 
        'apartment':apartment,
        'current_date':current_date
    }

    if request.method == "POST":
        print(request.POST)
        form = RentPaymentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            # redirect
            content = {
                'status':'OK',
                'statusCode':200,
                'message':'Success'
            }

            return HttpResponse(json.dumps(content))
        else:
            content = {
                'statusCode':403,
                'message':"Error",
                'status':'Denied',
                'errors':form.errors
            }

            return HttpResponse(json.dumps(content))

    if request.GET.get('print') == "True":
        pdf = render_to_pdf("property/rent/receipt.html", context)
        print(pdf)
        return HttpResponse(pdf, content_type='application/pdf')

    return render(request, "property/rent/payment.html", context)
  

# def commit_payment(request, payment_mode):
#     payment_form = RentPaymentForm(
#         receipt_number=receipt_number,
#         amout_paid=tenant.rent_charge,
#         payment_mode=payment_mode
#     )

#     if form.is_valid():
#         payment = payment_form.save(commit=False)
#         payment.receipt

#         return HttpResponse({"message":"successfully paid"})


def link_callback(uri, rel):
    if not os.path.isfile(uri):
        raise Exception('File not found')
    return uri
    
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    pdf = pisa.CreatePDF(html, dest=response, link_callback=link_callback)

    if not pdf.err:
        # return HttpResponse(result.getvalue(), content_type='application/pdf')
        return response

    return None