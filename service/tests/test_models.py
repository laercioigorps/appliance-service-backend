from django.test import TestCase
from service.models import Service

from profiles.tests.factories import (
    AddressFactory,
    CustomerFactory,
    OrganizationFactory,
)
from appliances.tests.factories import HistoricFactory, SymptomFactory


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

    def test_add_address_to_service(self):
        self.assertEqual(self.service.address, None)
        self.service.address = self.customer.address.first()
        self.assertEqual(
            self.service.address.number, self.customer.address.first().number
        )

    def test_add_symptoms_to_service_historic(self):
        symptomCount = self.service.historic.symptoms.all().count()
        symptom1 = SymptomFactory()
        symptom2 = SymptomFactory()

        self.service.historic.symptoms.add(symptom1)
        self.service.historic.symptoms.add(symptom2)

        newSymptomCount = self.service.historic.symptoms.all().count()
        self.assertEqual(newSymptomCount, symptomCount + 2)
