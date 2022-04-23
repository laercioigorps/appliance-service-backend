from django.contrib import admin

from appliances.models import Appliance, Brand, Category, Symptom, Problem, Solution

# Register your models here.

admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Appliance)

admin.site.register(Symptom)
admin.site.register(Problem)
admin.site.register(Solution)
