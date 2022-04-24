from django.db import models

# Create your models here.
class Address(models.Model):
    number = models.CharField(max_length=10)
    street = models.CharField(max_length=30)
    neighborhood = models.CharField(max_length=30)
    city = models.CharField(max_length=30, null=True)
    state = models.CharField(max_length=30, null=True)
    country = models.CharField(max_length=30, default="Brasil")
    coordinates = models.CharField(max_length=30, null=True)
    complement = models.CharField(max_length=40, null=True)
    is_active = models.BooleanField(default=True)
    type = models.CharField(max_length=30, null=True)


class Organization(models.Model):
    name = models.CharField(max_length=30)


class Customer(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(Organization, on_delete=models.CASCADE)
