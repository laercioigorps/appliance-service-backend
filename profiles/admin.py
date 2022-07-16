from django.contrib import admin
from .models import Customer, Organization

# Register your models here.

admin.site.register(Customer)
admin.site.register(Organization)