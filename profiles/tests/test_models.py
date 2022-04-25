from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import Address, Organization, Customer, Profile

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


class TestCustomer(TestCase):
    def setUp(self) -> None:
        self.organization1 = Organization.objects.create(name="TestOrganization")

    def test_create_customer_with_organization(self):
        customer_count = Customer.objects.all().count()
        self.assertEqual(customer_count, 0)

        customer = Customer.objects.create(
            name="first customer", owner=self.organization1
        )

        customer_count = Customer.objects.all().count()
        self.assertEqual(customer_count, 1)


class TestProfile(TestCase):
    def test_create_profile_by_creating_user(self):
        profile_count = Profile.objects.all().count()
        self.assertEqual(profile_count, 0)

        newUser = User.objects.create_user(username="paulo")

        profile_count = Profile.objects.all().count()
        self.assertEqual(profile_count, 1)
