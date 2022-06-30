from django.test import TestCase
from django.urls import reverse
from profiles.tests.factories import AddressFactory, CustomerFactory, UserFactory
from service.models import Service
from rest_framework.test import APIClient
import io
from rest_framework.parsers import JSONParser

from service.tests.factories import ServiceFactory


class ServiceViewTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()

        self.user1Client = APIClient()
        self.user1Client.force_authenticate(user=self.user1)

        self.user2Client = APIClient()
        self.user2Client.force_authenticate(user=self.user2)

        self.customer1 = CustomerFactory(
            owner=self.user1.profile.org, addresses=(AddressFactory(), AddressFactory())
        )
        self.service1 = ServiceFactory(
            owner=self.user1.profile.org,
            customer=self.customer1,
            address=self.customer1.addresses.first(),
        )

        customer2 = CustomerFactory(
            owner=self.user2.profile.org, addresses=(AddressFactory(), AddressFactory())
        )
        self.service2 = ServiceFactory(
            owner=self.user2.profile.org,
            customer=customer2,
            address=customer2.addresses.first(),
        )

        self.service3 = ServiceFactory(owner=self.user1.profile.org)

        self.notAuthenticatedClient = APIClient()

    def test_list_services_by_user_org(self):
        serviceCount = Service.objects.filter(owner=self.user1.profile.org).count()
        self.assertEqual(serviceCount, 2)

        response = self.user1Client.get(reverse("service:service_list"), format="json")

        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 2)

        self.assertEqual(data[0]["customer"]["name"], self.service1.customer.name)
        self.assertEqual(data[0]["address"]["number"], self.service1.address.number)
        self.assertEqual(data[0]["price"], str(self.service1.price))

    def test_list_services_with_not_authenticated_user(self):
        response = self.notAuthenticatedClient.get(
            reverse("service:service_list"), format="json"
        )
        self.assertEqual(response.status_code, 403)

    def test_create_service_only_with_required_data(self):
        serviceCount = Service.objects.filter(owner=self.user1.profile.org).count()
        self.assertEqual(serviceCount, 2)

        response = self.user1Client.post(reverse("service:service_list"), format="json")

        self.assertEqual(response.status_code, 201)

        serviceCount = Service.objects.filter(owner=self.user1.profile.org).count()
        self.assertEqual(serviceCount, 3)

    def test_create_service_with_not_authenticated_user(self):
        response = self.notAuthenticatedClient.post(
            reverse("service:service_list"), format="json"
        )
        self.assertEqual(response.status_code, 403)

    def test_get_service_detail_with_valid_user(self):
        response = self.user1Client.get(
            reverse("service:service_detail", kwargs={"service_pk": self.service1.id}),
            format="json",
        )
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data["customer"]["name"], self.service1.customer.name)
        self.assertEqual(data["address"]["number"], self.service1.address.number)
        self.assertEqual(data["price"], str(self.service1.price))

    def test_get_service_detail_with_not_authenticated_user(self):
        response = self.notAuthenticatedClient.get(
            reverse("service:service_detail", kwargs={"service_pk": self.service1.id}),
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_get_not_valid_service_detail_with_authenticated_user(self):
        response = self.user1Client.get(
            reverse("service:service_detail", kwargs={"service_pk": 100}),
            format="json",
        )
        self.assertEqual(response.status_code, 404)

    def test_get_service_detail_wich_the_user_does_not_own(self):
        response = self.user2Client.get(
            reverse("service:service_detail", kwargs={"service_pk": self.service1.id}),
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_create_service_for_valid_user(self):
        serviceCount = Service.objects.filter(customer=self.customer1).count()

        response = self.user1Client.post(
            reverse(
                "service:customer_service_list",
                kwargs={"customer_pk": self.customer1.id},
            ),
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        newServiceCount = Service.objects.filter(customer=self.customer1).count()
        self.assertEqual(newServiceCount, serviceCount + 1)
