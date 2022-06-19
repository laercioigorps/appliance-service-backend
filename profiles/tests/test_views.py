from django import views
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import io
from rest_framework.parsers import JSONParser

from profiles.models import Address, Customer


class TestCustomerView(TestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create_user("root1", "email1@exemple.com", "root")
        self.user2 = User.objects.create_user("root2", "email2@exemple.com", "root")

        self.customer1 = Customer.objects.create(
            name="josé", owner=self.user2.profile.org
        )
        self.customer2 = Customer.objects.create(
            name="Maria", owner=self.user2.profile.org
        )
        self.customer3 = Customer.objects.create(
            name="Pedro", owner=self.user2.profile.org
        )
        self.customer4 = Customer.objects.create(
            name="Pedro", owner=self.user1.profile.org
        )

    def test_create_customer(self):
        customer_count = Customer.objects.all().count()
        self.assertEqual(customer_count, 4)

        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.post(
            reverse("profiles:customer_list"), {"name": "customer1"}, format="json"
        )
        self.assertEqual(response.status_code, 201)

        customer_count = Customer.objects.all().count()
        self.assertEqual(customer_count, 5)

    def test_list_customer_by_user_organization(self):
        customer_owned_by_user2_organization = Customer.objects.filter(
            owner=self.user2.profile.org
        ).count()
        self.assertEqual(customer_owned_by_user2_organization, 3)

        client = APIClient()
        client.force_authenticate(user=self.user2)
        response = client.get(reverse("profiles:customer_list"))
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 3)


class TestCustomerDetailView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user("root1", "email1@exemple.com", "root")
        self.user2 = User.objects.create_user("root2", "email2@exemple.com", "root")

        self.customer1 = Customer.objects.create(
            name="josé", owner=self.user2.profile.org
        )
        self.customer2 = Customer.objects.create(
            name="Maria", owner=self.user2.profile.org
        )
        self.customer3 = Customer.objects.create(
            name="Pedro", owner=self.user2.profile.org
        )
        self.customer4 = Customer.objects.create(
            name="Pedro", owner=self.user1.profile.org
        )

    def test_get_customer_with_valid_user(self):
        client = APIClient()
        client.force_authenticate(self.user1)

        response = client.get(
            reverse("profiles:customer_detail", kwargs={"pk": self.customer4.id}),
            format="json",
        )

        self.assertEquals(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data["name"], self.customer4.name)

    def test_get_customer_with_not_authenticated_user(self):
        client = APIClient()

        response = client.get(
            reverse("profiles:customer_detail", kwargs={"pk": self.customer4.id}),
            format="json",
        )

        self.assertEquals(response.status_code, 403)

    def test_get_invalid_customer_with_authenticated_user(self):
        client = APIClient()
        client.force_authenticate(self.user1)
        response = client.get(
            reverse("profiles:customer_detail", kwargs={"pk": 100}),
            format="json",
        )

        self.assertEquals(response.status_code, 404)

    def test_get_customer_wich_authenticated_user_dont_own(self):
        client = APIClient()
        client.force_authenticate(self.user1)
        response = client.get(
            reverse("profiles:customer_detail", kwargs={"pk": self.customer1.id}),
            format="json",
        )

        self.assertEquals(response.status_code, 403)

    def test_update_customer_with_authenticated_user(self):
        client = APIClient()
        client.force_authenticate(self.user2)
        response = client.put(
            reverse("profiles:customer_detail", kwargs={"pk": self.customer1.id}),
            {"name": "new name", "owner": self.customer1.owner.id},
            format="json",
        )

        self.assertEquals(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data["name"], "new name")


class TestAddressView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user("root1", "email1@exemple.com", "root")
        self.user2 = User.objects.create_user("root2", "email2@exemple.com", "root")

        self.customer1 = Customer.objects.create(
            name="josé", owner=self.user2.profile.org
        )
        self.customer2 = Customer.objects.create(
            name="Maria", owner=self.user2.profile.org
        )
        self.customer3 = Customer.objects.create(
            name="Pedro", owner=self.user2.profile.org
        )

    def test_create_address_to_custumer_with_authenticated_user(self):
        addressCount = self.customer1.address.count()
        self.assertEqual(addressCount, 0)

        client = APIClient()
        client.force_authenticate(user=self.user2)

        response = client.post(
            reverse("profiles:customer_address_list", kwargs={"pk": self.customer1.id}),
            {
                "number": "5",
                "street": "street1",
                "neighborhood": "neighb",
                "city": "San Andreas",
            },
            format="json",
        )
        self.assertEquals(response.status_code, 201)

        addressCount = self.customer1.address.count()
        self.assertEqual(addressCount, 1)

    def test_create_address_to_custumer_with_not_authenticated_user(self):
        addressCount = self.customer2.address.count()
        self.assertEqual(addressCount, 0)

        client = APIClient()

        response = client.post(
            reverse("profiles:customer_address_list", kwargs={"pk": self.customer2.id}),
            {
                "number": "5",
                "street": "street1",
                "neighborhood": "neighb",
                "city": "San Andreas",
            },
            format="json",
        )
        self.assertEquals(response.status_code, 403)

        addressCount = self.customer2.address.count()
        self.assertEqual(addressCount, 0)

    def test_create_address_to_custumer_wich_the_user_organization_not_own(self):
        addressCount = self.customer2.address.count()
        self.assertEqual(addressCount, 0)

        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.post(
            reverse("profiles:customer_address_list", kwargs={"pk": self.customer2.id}),
            {
                "number": "5",
                "street": "street1",
                "neighborhood": "neighb",
                "city": "San Andreas",
            },
            format="json",
        )
        self.assertEquals(response.status_code, 403)

        addressCount = self.customer2.address.count()
        self.assertEqual(addressCount, 0)

    def test_create_address_to_invalid_customer_with_authenticated_user(self):
        addressCount = Address.objects.all().count()
        self.assertEquals(addressCount, 0)

        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.post(
            reverse("profiles:customer_address_list", kwargs={"pk": 100}),
            {
                "number": "5",
                "street": "street1",
                "neighborhood": "neighb",
                "city": "San Andreas",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 404)

        addressCount = Address.objects.all().count()
        self.assertEquals(addressCount, 0)

    def test_create_address_to_custumer_with_not_valid_data(self):
        addressCount = self.customer1.address.count()
        self.assertEqual(addressCount, 0)

        client = APIClient()
        client.force_authenticate(user=self.user2)

        response = client.post(
            reverse("profiles:customer_address_list", kwargs={"pk": self.customer1.id}),
            {
                "street": "street1",
                "neighborhood": "neighb",
                "city": "San Andreas",
            },
            format="json",
        )
        self.assertEquals(response.status_code, 400)

        addressCount = self.customer1.address.count()
        self.assertEqual(addressCount, 0)


class TestAddressListGetView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user("root1", "email1@exemple.com", "root")
        self.user2 = User.objects.create_user("root2", "email2@exemple.com", "root")

        self.customer1 = Customer.objects.create(
            name="josé", owner=self.user2.profile.org
        )
        self.customer2 = Customer.objects.create(
            name="Maria", owner=self.user2.profile.org
        )
        self.customer3 = Customer.objects.create(
            name="Pedro", owner=self.user2.profile.org
        )

        self.address1 = Address.objects.create(
            number="1", street="street1", neighborhood="neigh1"
        )
        self.address2 = Address.objects.create(
            number="2", street="street2", neighborhood="neigh2"
        )
        self.address3 = Address.objects.create(
            number="3", street="street3", neighborhood="neigh3"
        )

        self.customer1.address.add(self.address1)
        self.customer1.address.add(self.address2)

        self.customer2.address.add(self.address3)

    def test_list_address_from_customer_with_authenticated_user(self):

        client = APIClient()
        client.force_authenticate(self.user2)

        response = client.get(
            reverse("profiles:customer_address_list", kwargs={"pk": self.customer1.id})
        )

        self.assertEquals(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(len(data), 2)

    def test_list_address_from_customer_with_not_authenticated_user(self):

        client = APIClient()

        response = client.get(
            reverse("profiles:customer_address_list", kwargs={"pk": self.customer1.id})
        )

        self.assertEquals(response.status_code, 403)

    def test_list_address_from_customer_with_invalid_customer_id(self):

        client = APIClient()
        client.force_authenticate(self.user1)

        response = client.get(
            reverse("profiles:customer_address_list", kwargs={"pk": 100})
        )

        self.assertEquals(response.status_code, 404)

    def test_list_address_from_customer_wich_the_user_does_not_own(self):

        client = APIClient()
        client.force_authenticate(self.user1)

        response = client.get(
            reverse("profiles:customer_address_list", kwargs={"pk": self.customer1.id})
        )

        self.assertEquals(response.status_code, 403)
