from locale import currency
from rest_framework import serializers

from profiles.models import Address, Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id","name", "owner", "addresses"]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id","number", "street", "neighborhood", "city"]
