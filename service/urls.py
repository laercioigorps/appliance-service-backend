from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = "service"

urlpatterns = [
    path("", views.ServiceListView.as_view(), name="service_list"),
    path("<int:service_pk>", views.ServiceDetailView.as_view(), name="service_detail"),
    path("customer/<int:customer_pk>", views.CustomerServiceListView.as_view(), name="customer_service_list"),

]

urlpatterns = format_suffix_patterns(urlpatterns)
