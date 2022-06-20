from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = "profiles"
urlpatterns = [
    path("customers/", views.customer_list_view, name="customer_list"),
    path("customers/<int:pk>", views.CustomerDetailView.as_view(), name="customer_detail"),
    path("customers/<int:pk>/address/", views.CustomerAddressListView.as_view(), name="customer_address_list"),
    path("customers/<int:pk>/address/<int:address_pk>/", views.CustomerAddressDetailView.as_view(), name="customer_address_detail")
]

urlpatterns = format_suffix_patterns(urlpatterns)
