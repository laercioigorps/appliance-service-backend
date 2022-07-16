import email
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import date

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
    addresses = models.ManyToManyField(Address, blank=True)
    email = models.EmailField(max_length=20, null=True, blank=True)
    nickname = models.CharField(max_length=30, null=True, blank=True)
    profession = models.CharField(max_length=20, null=True, blank=True)
    phone1 = models.CharField(max_length=15, null=True, blank=True)
    phone2 = models.CharField(max_length=15, null=True, blank=True)
    created_at = models.DateField(default=date.today())

    def has_object_permission(self, request):
        return self.owner == request.user.profile.org


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
