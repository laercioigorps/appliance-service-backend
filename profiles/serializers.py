from locale import currency
from rest_framework import serializers

from profiles.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["name", "owner", "address"]
