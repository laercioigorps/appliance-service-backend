from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = "profiles"
urlpatterns = [
    path("customers/", views.customer_list_view, name="customer_list"),
]

urlpatterns = format_suffix_patterns(urlpatterns)