from django.test import TestCase

from profiles.models import Address, Organization

# Create your tests here.
class TestAddress(TestCase):
    def test_create_address(self):
        address_count = Address.objects.all().count()
        self.assertEqual(address_count, 0)

        address = Address.objects.create(street="xyz", number="k")

        address_count = Address.objects.all().count()
        self.assertEqual(address_count, 1)


class TestOrganization(TestCase):
    def test_create_organizarion(self):
        organization_count = Organization.objects.all().count()
        self.assertEqual(organization_count, 0)

        org = Organization.objects.create(name="TestOrganization")

        organization_count = Organization.objects.all().count()
        self.assertEqual(organization_count, 1)
