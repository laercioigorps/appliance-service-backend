from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import Address, Organization, Customer, Profile
from .factories import AddressFactory, CustomerFactory, OrganizationFactory, UserFactory

# Create your tests here.
class TestAddress(TestCase):
    def test_create_address(self):
        address_count = Address.objects.all().count()
        self.assertEqual(address_count, 0)

        address = Address.objects.create(street="xyz", number="k")

        address_count = Address.objects.all().count()
        self.assertEqual(address_count, 1)

    def test_create_address_using_factory(self):
        address_count = Address.objects.all().count()

        address = AddressFactory()

        newAddress_count = Address.objects.all().count()
        self.assertEqual(newAddress_count, address_count + 1)


class TestOrganization(TestCase):
    def test_create_organizarion(self):
        organization_count = Organization.objects.all().count()
        self.assertEqual(organization_count, 0)

        org = Organization.objects.create(name="TestOrganization")

        organization_count = Organization.objects.all().count()
        self.assertEqual(organization_count, 1)

    def test_create_organizarion_using_factory(self):
        organization_count = Organization.objects.all().count()

        org = OrganizationFactory()

        newOrganization_count = Organization.objects.all().count()
        self.assertEqual(newOrganization_count, organization_count + 1)


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

    def test_create_customer_with_organization_using_factory(self):
        customer_count = Customer.objects.all().count()

        customer = CustomerFactory()

        newCustomer_count = Customer.objects.all().count()
        self.assertEqual(newCustomer_count, customer_count + 1)

    def test_add_address_to_customer(self):
        address = Address.objects.create(
            street="street1", neighborhood="caic", number="5"
        )
        customer = Customer.objects.create(
            name="first customer", owner=self.organization1
        )
        customer.addresses.add(address)

        c = Customer.objects.get(pk=customer.pk)
        a = c.addresses.first()
        self.assertEqual(a.street, "street1")
        self.assertEqual(a.neighborhood, "caic")
        self.assertEqual(a.number, "5")

    def test_add_two_address_to_customer(self):
        address1 = Address.objects.create(
            street="street1", neighborhood="caic1", number="1"
        )
        address2 = Address.objects.create(
            street="street2", neighborhood="caic2", number="2"
        )

        customer = Customer.objects.create(
            name="first customer", owner=self.organization1
        )

        address_count = customer.addresses.count()
        self.assertEqual(address_count, 0)

        customer.addresses.add(address1)

        address_count = customer.addresses.count()
        self.assertEqual(address_count, 1)

        customer.addresses.add(address2)

        address_count = customer.addresses.count()
        self.assertEqual(address_count, 2)

    def test_add_two_address_to_customer_using_factory(self):

        customer = CustomerFactory(addresses=(AddressFactory(), AddressFactory()))

        customer_address_count = customer.addresses.all().count()
        self.assertEqual(customer_address_count, 2)


class TestProfile(TestCase):
    def test_create_profile_by_creating_user(self):
        profile_count = Profile.objects.all().count()
        self.assertEqual(profile_count, 0)

        newUser = User.objects.create_user(username="paulo")

        profile_count = Profile.objects.all().count()
        self.assertEqual(profile_count, 1)

    def test_create_profile_by_creating_user_using_factory(self):
        profile_count = Profile.objects.all().count()

        newUser = UserFactory()

        newProfile_count = Profile.objects.all().count()
        self.assertEqual(newProfile_count, profile_count + 1)

    def test_create_profile_and_verity_own_organization(self):
        organization_count = Organization.objects.all().count()
        self.assertEqual(organization_count, 0)

        newUser = User.objects.create_user(username="paulo")

        organization_count = Organization.objects.all().count()
        self.assertEqual(organization_count, 1)

        self.assertEqual(newUser.profile.org.name, "own")
