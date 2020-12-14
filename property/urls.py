from django.urls import path
from .views import home, detail_view, get_property
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('', home, name="home"),
  path('detail/<slug:title>', detail_view, name="detail-view"),
  path('property-data/', get_property, name="property")
]

if settings.DEBUG:
    urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
