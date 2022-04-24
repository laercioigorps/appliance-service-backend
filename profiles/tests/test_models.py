from django.test import TestCase

from profiles.models import Address

# Create your tests here.
class TestAddress(TestCase):
    def test_create_address(self):
        address_count = Address.objects.all().count()
        self.assertEqual(address_count, 0)

        address = Address.objects.create(street="xyz", number="k")

        address_count = Address.objects.all().count()
        self.assertEqual(address_count, 1)
