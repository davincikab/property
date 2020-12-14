from django.contrib.gis import admin
from .models import Property, PropertyImage

# Register your models here.
admin.site.register(Property, admin.GeoModelAdmin)
admin.site.register(PropertyImage)