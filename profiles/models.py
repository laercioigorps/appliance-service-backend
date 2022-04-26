from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

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
    address = models.ManyToManyField(Address, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    org = models.ForeignKey(
        Organization, on_delete=models.CASCADE, null=True, blank=True
    )

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            organization = Organization.objects.create(name="own")
            profile = Profile.objects.create(user=instance, org=organization)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
