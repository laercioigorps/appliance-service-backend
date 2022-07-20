from django.contrib import admin

from service.models import Service, Status

# Register your models here.

admin.site.register(Status)
admin.site.register(Service)
