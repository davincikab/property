from django.urls import path
from .views import home, detail_view, get_property, create_property, update_property, delete_property, filter_property
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('', home, name="home"),
  path("filter-property", filter_property , name="filter-property"),
  path('property-data/', get_property, name="property"),
  path('detail/<slug:title>', detail_view, name="detail-view"),
  path('create/',create_property , name="create-property"),
  path('update/<slug:title>', update_property, name="update-property"),
   path('delete/<slug:title>', delete_property, name="delete-property"),
]

if settings.DEBUG:
    urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
