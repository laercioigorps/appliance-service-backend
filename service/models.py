from django.db import models
from profiles.models import Address, Customer, Organization
from appliances.models import Historic
from datetime import date

# Create your models here.


class Status(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=70)
    is_conclusive = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


class Service(models.Model):
    owner = models.ForeignKey(Organization, on_delete=models.CASCADE)
    historic = models.ForeignKey(Historic, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    start_date = models.DateField(default=date.today())
    end_date = models.DateField(null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
