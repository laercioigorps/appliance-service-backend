from django.db import models

from appliances.models import Historic
from profiles.models import Address, Customer, Organization

# Create your models here.
class Service(models.Model):
    history = models.ForeignKey(Historic, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, blank=True, null=True
    )
