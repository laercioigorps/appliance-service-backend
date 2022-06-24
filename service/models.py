from django.db import models
from profiles.models import Customer, Organization
from appliances.models import Historic

# Create your models here.

class Service(models.Model):
    owner = models.ForeignKey(Organization, on_delete=models.CASCADE)
    historic = models.ForeignKey(Historic, on_delete=models.CASCADE)
