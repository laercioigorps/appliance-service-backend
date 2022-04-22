from django.contrib import admin

from appliances.models import Appliance, Brand, Category

# Register your models here.

admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Appliance)
