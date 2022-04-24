from django.test import TestCase
from appliances.models import Historic

from profiles.models import Customer, Organization
from services.models import Service


# Create your tests here.
class ServiceTest(TestCase):
    def setUp(self) -> None:
        self.organization = Organization.objects.create()
        self.customer1 = Customer.objects.create(
            name="client1", owner=self.organization
        )
        self.historic = Historic.objects.create()

    def test_create_basic_service_without_address(self):
        service_count = Service.objects.all().count()
        self.assertEqual(service_count, 0)

        service = Service.objects.create(
            history=self.historic,
            organization=self.organization,
            customer=self.customer1,
        )

        service_count = Service.objects.all().count()
        self.assertEqual(service_count, 1)
