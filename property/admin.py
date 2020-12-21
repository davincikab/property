from django.contrib.gis import admin
from .models import Property, PropertyImage, Apartment, Tenants, RentPayment

# Register your models here.
admin.site.register(Property, admin.GeoModelAdmin)
admin.site.register(PropertyImage)

@admin.register(Apartment)
class ApartmentAdmin(admin.GeoModelAdmin):
    list_display = ("name", "units", "owner", "occupied_units",)
    search_fields = ["name", "owner"]

@admin.register(Tenants)
class TenantsAdmin(admin.GeoModelAdmin):
    list_display = ("first_name", "last_name",  "id_number", "apartment")
    list_filter = ("marital_status", "room_type", "apartment")
    search_fields = ["first_name", "last_name"]

@admin.register(RentPayment)
class RentPaymentAdmin(admin.GeoModelAdmin):
    list_display = ("receipt_number", "tenant", "payment_mode", "paid_on",)
    list_filter = ("payment_mode",)
    search_fields = ["receipt_number",]