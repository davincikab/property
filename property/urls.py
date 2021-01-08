from django.urls import path
from .views import home, detail_view, get_property, create_property, update_property, delete_property, filter_property, \
  list_tenants, list_apartment , ApartmentDetailView, filter_apartment, apartment_data, create_apartment, update_apartment, \
  delete_apartment, TenantDetailView, TenantsCreateView, TenantsDeleteView, TenantsUpdateView, make_payment

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('', home, name="home"),
  path("filter-property", filter_property , name="filter-property"),
  path('property-data/', get_property, name="property"),
  path('property/detail/<slug:title>', detail_view, name="detail-view"),
  path('property/<slug:title>/create/',create_property , name="create-property"),
  path('property/update/<slug:title>', update_property, name="update-property"),
  path('property/delete/<slug:title>', delete_property, name="delete-property"),

  # tenants tenants/{{object.apartment.slug}}/update/{{object.pk}}
  path("tenants/", list_tenants, name="tenants"),
  path("tenants/<int:pk>/", TenantDetailView.as_view(), name="tenants-detail"),
  path("tenants/<slug:title>/create/", TenantsCreateView.as_view(), name="tenants-create"),
  path("tenants/<slug:title>/update/<int:pk>/", TenantsUpdateView.as_view(), name="tenants-update"),
  path("tenants/<slug:title>/delete/<int:pk>/", TenantsDeleteView.as_view(), name="tenants-update"),

  # apartments
  path("apartments/", list_apartment, name="apartments"),
  path("apartments-data/", apartment_data, name="apartment-data"),
  path("apartments-list/", filter_apartment, name="list-apartments"),
  path("apartments/<int:pk>/", ApartmentDetailView.as_view(), name="apartment-detail"),
  path("apartments/create/", create_apartment, name="create-apartments"),
  path("apartments-update/<int:pk>/", update_apartment, name="update-apartments"),
  path("apartments/delete/<int:pk>/", delete_apartment, name="delete-apartments"),

  # payment
  path("make-payment/<slug:title>/<int:tenant_id>/", make_payment, name="make-payments"),
]

if settings.DEBUG:
    urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
