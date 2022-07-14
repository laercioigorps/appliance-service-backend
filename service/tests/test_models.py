from datetime import date
from django.test import TestCase
from service.models import Service
from datetime import date

from service.tests.factories import (
    AddressFactory,
    CustomerFactory,
    OrganizationFactory,
    ServiceFactory,
)
from appliances.tests.factories import (
    HistoricFactory,
    ProblemFactory,
    SolutionFactory,
    SymptomFactory,
)

from decimal import Decimal


class ServiceModelTest(TestCase):
    def setUp(self):
        self.org = OrganizationFactory()
        self.customer = CustomerFactory(
            addresses=(AddressFactory(), AddressFactory()), owner=self.org
        )
        self.address = self.customer.addresses.first()
        self.historic = HistoricFactory(org=self.org)
        self.service = Service.objects.create(owner=self.org, historic=self.historic)

    def test_create_service_only_with_required_data(self):
        service_count = Service.objects.all().count()
        service = Service.objects.create(owner=self.org, historic=self.historic)
        newServiceCount = Service.objects.all().count()
        self.assertEqual(newServiceCount, service_count + 1)

    def test_create_service_using_factory(self):
        service_count = Service.objects.all().count()
        service = ServiceFactory()
        newServiceCount = Service.objects.all().count()
        self.assertEqual(newServiceCount, service_count + 1)

    def test_add_customer_to_service(self):
        self.assertEqual(self.service.customer, None)
        self.service.customer = self.customer
        self.assertEqual(self.service.customer.name, self.customer.name)

    def test_create_service_using_factory_with_the_same_customer_org(self):
        service = ServiceFactory()
        self.assertEqual(service.owner.id, service.customer.owner.id)

    def test_create_service_using_factory_with_the_same_customer_org_passing_at_creation(
        self,
    ):
        org = OrganizationFactory()
        service = ServiceFactory(owner=org)
        self.assertEqual(service.owner.id, service.customer.owner.id)

    def test_create_service_using_factory_with_the_same_historic_org(self):
        service = ServiceFactory()
        self.assertEqual(service.owner.id, service.historic.org.id)

    def test_add_address_to_service(self):
        self.assertEqual(self.service.address, None)
        self.service.address = self.customer.addresses.first()
        self.assertEqual(
            self.service.address.number, self.customer.addresses.first().number
        )

    def test_add_symptoms_to_service_historic(self):
        symptomCount = self.service.historic.symptoms.all().count()
        symptom1 = SymptomFactory()
        symptom2 = SymptomFactory()

        self.service.historic.symptoms.add(symptom1)
        self.service.historic.symptoms.add(symptom2)

        newSymptomCount = self.service.historic.symptoms.all().count()
        self.assertEqual(newSymptomCount, symptomCount + 2)

    def test_add_problems_to_service_historic(self):
        problemCount = self.service.historic.problems.all().count()
        problem1 = ProblemFactory()
        problem2 = ProblemFactory()

        self.service.historic.problems.add(problem1)
        self.service.historic.problems.add(problem2)

        newproblemCount = self.service.historic.problems.all().count()
        self.assertEqual(newproblemCount, problemCount + 2)

    def test_add_solutions_to_service_historic(self):
        solutionCount = self.service.historic.solutions.all().count()
        solution1 = SolutionFactory()
        solution2 = SolutionFactory()

        self.service.historic.solutions.add(solution1)
        self.service.historic.solutions.add(solution2)

        newSolutionCount = self.service.historic.solutions.all().count()
        self.assertEqual(newSolutionCount, solutionCount + 2)

    def test_service_starting_date(self):
        today = date.today()
        self.assertEqual(self.service.start_date, today)

    def test_service_price_with_new_service(self):
        self.assertEqual(self.service.price, 0)
        self.service.price = Decimal("120.2")
        self.service.save()
        self.assertEqual(self.service.price, Decimal("120.2"))

    def test_service_price_with_bing_number(self):
        self.assertEqual(self.service.price, 0)
        self.service.price = Decimal("9999.21")
        self.service.save()
        self.assertEqual(self.service.price, Decimal("9999.21"))

    def test_service_start_date(self):
        service = ServiceFactory()
        self.assertIsNotNone(service.start_date)
