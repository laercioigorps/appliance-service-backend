from django.test import TestCase
from service.models import Service

from profiles.tests.factories import (
    AddressFactory,
    CustomerFactory,
    OrganizationFactory,
)
from appliances.tests.factories import HistoricFactory


class ServiceModelTest(TestCase):
    def setUp(self):
        self.org = OrganizationFactory()
        self.customer = CustomerFactory(
            address=(AddressFactory(), AddressFactory()), owner=self.org
        )
        self.address = self.customer.address.first()
        self.historic = HistoricFactory(org=self.org)
        self.service = Service.objects.create(owner=self.org, historic=self.historic)

    def test_create_service_only_with_required_data(self):
        service_count = Service.objects.all().count()
        service = Service.objects.create(owner=self.org, historic=self.historic)
        newServiceCount = Service.objects.all().count()
        self.assertEqual(newServiceCount, service_count + 1)

    def test_add_customer_to_service(self):
        self.assertEqual(self.service.customer, None)
        self.service.customer = self.customer
        self.assertEqual(self.service.customer.name, self.customer.name)

