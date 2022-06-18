from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import io
from rest_framework.parsers import JSONParser

from profiles.models import Customer


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
        customer_owned_by_user2_organization = Customer.objects.filter(owner= self.user2.profile.org).count()
        self.assertEqual(customer_owned_by_user2_organization, 3)

        client = APIClient()
        client.force_authenticate(user=self.user2)
        response = client.get(reverse("profiles:customer_list"))
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 3)


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
