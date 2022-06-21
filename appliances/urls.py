from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = "appliances"

urlpatterns = [
    path("appliances/brands/", views.BrandListView.as_view(), name="brand_list"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
