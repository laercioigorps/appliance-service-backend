from datetime import date, timedelta
from django.test import TestCase
from appliances.models import Appliance, Brand, Category, Symptom
from appliances.tests.factories import BrandFactory, CategoryFactory
from service.models import Service, Status
from profiles.models import Address, Customer, Organization

from service.services import InitialSampleDataCreation, SampleDataCreation


class SampleInitialDataCreationTest(TestCase):
    def setUp(self):
        self.sampleData = InitialSampleDataCreation()

    def test_initial_sample_data_setUp(self):
        self.assertIsNotNone(self.sampleData)

    def test_initial_brands(self):
        self.assertEqual(len(self.sampleData.brands), 0)

    def test_initial_categories(self):
        self.assertEqual(len(self.sampleData.categories), 0)

    def test_initial_appliances(self):
        self.assertEqual(len(self.sampleData.appliances), 0)

    def test_initial_symptoms(self):
        self.assertEqual(len(self.sampleData.symptoms), 0)

    def test_initial_problems(self):
        self.assertEqual(len(self.sampleData.problems), 0)

    def test_initial_solutions(self):
        self.assertEqual(len(self.sampleData.solutions), 0)

    def test_initial_statuses(self):
        self.assertEqual(len(self.sampleData.statuses), 0)

    def test_generate_5_random_brands(self):
        self.sampleData.generateRandomBrands(5)
        self.assertEqual(len(self.sampleData.brands), 5)

    def test_generate_5_random_categories(self):
        self.sampleData.generateRandomCategories(5)
        self.assertEqual(len(self.sampleData.categories), 5)

    def test_generate_5_random_appliances_with_generated_categories_and_brands(self):
        self.sampleData.generateRandomBrands(3)
        self.sampleData.generateRandomCategories(3)
        self.sampleData.generateRandomAppliances(5)
        self.assertEqual(len(self.sampleData.appliances), 5)
        self.assertTrue(self.sampleData.appliances[0].brand in self.sampleData.brands)
        self.assertTrue(
            self.sampleData.appliances[0].category in self.sampleData.categories
        )

    def test_generate_5_random_status(self):
        self.sampleData.generateRandonStatus(quantity=5)
        self.assertEqual(len(self.sampleData.statuses), 5)

    def test_set_1_random_status_as_conclusive(self):
        self.sampleData.generateRandonStatus(3)
        self.sampleData.setRandomStatusAsConclusive(1)
        is_conclusive = False
        for status in self.sampleData.statuses:
            if status.is_conclusive:
                is_conclusive = True
                break
        self.assertTrue(is_conclusive)

    def test_set_status_manually(self):
        myStatus = []
        for i in range(3):
            myStatus.append(Status.objects.create(name="test", description="test"))
        self.sampleData.statuses = myStatus
        self.assertEqual(myStatus, self.sampleData.statuses)

    def test_generate_10_random_symptoms(self):
        self.sampleData.generateRandomSymptoms(10)
        self.assertEqual(len(self.sampleData.symptoms), 10)

    def test_generate_10_random_problems(self):
        self.sampleData.generateRandomProblems(10)
        self.assertEqual(len(self.sampleData.problems), 10)

    def test_generate_10_random_solutions(self):
        self.sampleData.generateRandomSolutions(10)
        self.assertEqual(len(self.sampleData.solutions), 10)


class SampleDataCreationServiceTest(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name="own")
        self.sampleData = SampleDataCreation()
        self.initialData = InitialSampleDataCreation()
        self.sampleData.organization = self.organization
        self.setTestStatuses()
        self.generateInitialData()
        self.sampleData.fetchInitialData()

    def generateInitialData(self):
        self.initialData.generateRandomBrands(3)
        self.initialData.generateRandomCategories(3)
        self.initialData.generateRandomAppliances(5)
        self.initialData.generateRandomSymptoms(10)
        self.initialData.generateRandomProblems(10)
        self.initialData.generateRandomSolutions(10)
        self.initialData.statuses = list(Status.objects.all())

    def setTestStatuses(self):
        self.awaiting = Status.objects.create(
            name="Scheduled visit", description="Scheduled visit"
        )
        self.completed = Status.objects.create(
            name="Waiting for approval", description="Waiting for approval"
        )
        self.completed = Status.objects.create(
            name="Scheduled service", description="Scheduled service"
        )
        self.completed = Status.objects.create(
            name="Awaiting payment", description="Awaiting payment"
        )
        self.completed = Status.objects.create(
            name="Concluded", description="Concluded", is_conclusive=True
        )
        self.completed = Status.objects.create(name="Canceled", description="Canceled")

    def test_default_initial_values(self):
        myData = SampleDataCreation()
        self.assertEqual(len(myData.appliances), 0)
        self.assertEqual(len(myData.statuses), 0)
        self.assertEqual(len(myData.symptoms), 0)
        self.assertEqual(len(myData.problems), 0)
        self.assertEqual(len(myData.solutions), 0)

        self.assertEqual(len(myData.customers), 0)
        self.assertEqual(len(myData.services), 0)

    def test_set_organization(self):
        self.sampleData.organization = self.organization
        self.assertEqual(self.sampleData.organization, self.organization)

    def test_fetched_initial_data(self):
        self.sampleData.fetchInitialData()
        self.assertCountEqual(self.sampleData.statuses, self.initialData.statuses)
        self.assertCountEqual(self.sampleData.appliances, self.initialData.appliances)
        self.assertCountEqual(self.sampleData.symptoms, self.initialData.symptoms)
        self.assertCountEqual(self.sampleData.problems, self.initialData.problems)
        self.assertCountEqual(self.sampleData.solutions, self.initialData.solutions)

    def test_generate_10_customers(self):
        self.sampleData.generateRandomCustomers(10)
        self.assertEqual(len(self.sampleData.customers), 10)
        self.assertEqual(self.sampleData.customers[0].owner, self.organization)

    def test_generate_2_address_for_every_customer(self):
        self.sampleData.generateRandomCustomers(10)
        addressCount = Address.objects.count()
        self.assertEqual(addressCount, 0)
        self.sampleData.generateRandomAddressForCustomers(2)
        addressCount = Address.objects.count()
        self.assertEqual(addressCount, 20)
        testCustomer = Customer.objects.all().first()
        self.assertEqual(testCustomer.addresses.count(), 2)

    def test_generate_10_random_services(self):
        self.sampleData.generateRandomCustomers(2)
        self.sampleData.generateRandomAddressForCustomers(1)
        self.sampleData.generateRandomServices(10)
        serviceCount = Service.objects.count()
        self.assertEqual(serviceCount, 10)

    def test_generate_3_random_services_with_provided_organization(self):
        self.sampleData.generateRandomCustomers(1)
        self.sampleData.generateRandomAddressForCustomers(1)
        self.sampleData.generateRandomServices(3)
        sameOwner = True
        for service in self.sampleData.services:
            if service.owner != self.organization:
                sameOwner = False
                break
        self.assertTrue(sameOwner)

    def test_generate_3_random_services_with_provided_customers(self):
        self.sampleData.generateRandomCustomers(3)
        self.sampleData.generateRandomAddressForCustomers(1)
        self.sampleData.generateRandomServices(3)
        sameCustomers = True
        for service in self.sampleData.services:
            if service.customer not in self.sampleData.customers:
                sameCustomers = False
                break
        self.assertTrue(sameCustomers)

    def test_generate_3_random_services_with_2_symptoms_problems_and_solutions_each(
        self,
    ):
        self.sampleData.generateRandomCustomers(3)
        self.sampleData.generateRandomAddressForCustomers(2)
        self.sampleData.generateRandomServices(3)
        twoEachSymptoms = True
        twoEachProblems = True
        twoEachSolutions = True
        for service in self.sampleData.services:
            if service.historic.symptoms.count() != 2:
                twoEachSymptoms = False
            if service.historic.problems.count() != 2:
                twoEachProblems = False
            if service.historic.solutions.count() != 2:
                twoEachSolutions = False
        self.assertTrue(twoEachSymptoms)
        self.assertTrue(twoEachProblems)
        self.assertTrue(twoEachSolutions)

    def test_generate_3_random_services_with_symptoms_problems_and_solutions_initially_fetched(
        self,
    ):
        self.sampleData.generateRandomCustomers(3)
        self.sampleData.generateRandomAddressForCustomers(1)
        self.sampleData.generateRandomServices(3)
        symptomsInTheList = True
        problemsInTheList = True
        solutionsInTheList = True
        for service in self.sampleData.services:
            for symptom in service.historic.symptoms.all():
                if symptom not in self.sampleData.symptoms:
                    symptomsInTheList = False
            for problem in service.historic.problems.all():
                if problem not in self.sampleData.problems:
                    problemsInTheList = False
            for solution in service.historic.solutions.all():
                if solution not in self.sampleData.solutions:
                    solutionsInTheList = False
        self.assertTrue(symptomsInTheList)
        self.assertTrue(problemsInTheList)
        self.assertTrue(solutionsInTheList)

    def test_service_address_not_null(self):
        self.sampleData.generateRandomCustomers(3)
        self.sampleData.generateRandomAddressForCustomers(1)
        self.sampleData.generateRandomServices(3)
        notNullServices = True
        for service in self.sampleData.services:
            if not service.address:
                notNullServices = False
                break
        self.assertTrue(notNullServices)

    def test_service_address_is_the_same_as_customers(self):
        self.sampleData.generateRandomCustomers(3)
        self.sampleData.generateRandomAddressForCustomers(2)
        self.sampleData.generateRandomServices(5)
        sameAddress = True
        for service in self.sampleData.services:
            if service.address not in service.customer.addresses.all():
                sameAddress = False
                break
        self.assertTrue(sameAddress)

    def test_service_price_always_positive(self):
        self.sampleData.generateRandomCustomers(1)
        self.sampleData.generateRandomAddressForCustomers(1)
        self.sampleData.generateRandomServices(10)
        alwaysPositive = True
        for service in self.sampleData.services:
            if service.price < 0:
                alwaysPositive = False
                break
        self.assertTrue(alwaysPositive)

    def test_service_price_neve_greater_than_2000(self):
        self.sampleData.generateRandomCustomers(1)
        self.sampleData.generateRandomAddressForCustomers(1)
        self.sampleData.generateRandomServices(10)
        alwaysOk = True
        for service in self.sampleData.services:
            if service.price > 2000:
                alwaysOk = False
                break
        self.assertTrue(alwaysOk)

    def test_service_status_is_not_null(self):
        self.sampleData.generateRandomCustomers(1)
        self.sampleData.generateRandomAddressForCustomers(1)
        self.sampleData.generateRandomServices(3)
        statusNeverNull = True
        for service in self.sampleData.services:
            if not service.status:
                statusNeverNull = False
                break
        self.assertTrue(statusNeverNull)

    def test_service_with_conclusive_status_always_have_end_date(self):
        self.sampleData.generateRandomCustomers(1)
        self.sampleData.generateRandomAddressForCustomers(1)
        self.sampleData.generateRandomServices(10)
        conclusiveStatusAlwayHasEndDate = True
        for service in self.sampleData.services:
            if service.status.is_conclusive and not service.end_date:
                conclusiveStatusAlwayHasEndDate = False
                break
        self.assertTrue(conclusiveStatusAlwayHasEndDate)

    def test_services_service_date_in_2_months_before(self):
        startDate = date.today() - timedelta(days=30 * 2)
        endDate = date.today() - timedelta(days=30 * 1)

        self.sampleData.generateRandomCustomers(1)
        self.sampleData.generateRandomAddressForCustomers(1)

        self.sampleData.start_date = startDate
        self.sampleData.end_date = endDate

        self.sampleData.generateRandomServices(3)

        dateAlwaysBetween = True
        for service in self.sampleData.services:
            if service.start_date > endDate or service.start_date < startDate:
                print(service.start_date)
                dateAlwaysBetween = False
                break

        self.assertTrue(dateAlwaysBetween)

    def test_service_custumer_creation_date_in_date_range(self):
        startDate = date.today() - timedelta(days=30 * 2)
        endDate = date.today() - timedelta(days=30 * 1)

        self.sampleData.start_date = startDate
        self.sampleData.end_date = endDate

        self.sampleData.generateRandomCustomers(10)

        dateAlwaysBetween = True
        for customer in self.sampleData.customers:
            if customer.created_at > endDate or customer.created_at < startDate:
                dateAlwaysBetween = False
                break
        self.assertTrue(dateAlwaysBetween)


class SampleDataCreateColateralEffectsTest(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name="own")
        self.sampleData = SampleDataCreation()
        self.initialData = InitialSampleDataCreation()
        self.sampleData.organization = self.organization
        self.setTestStatuses()
        self.generateInitialData()
        self.sampleData.fetchInitialData()
        self.generateSampleData()

    def generateSampleData(self):
        self.sampleData.generateRandomCustomers(5)
        self.sampleData.generateRandomAddressForCustomers(2)
        self.sampleData.generateRandomServices(10)

    def generateInitialData(self):
        self.initialData.generateRandomBrands(3)
        self.initialData.generateRandomCategories(3)
        self.initialData.generateRandomAppliances(5)
        self.initialData.generateRandomSymptoms(10)
        self.initialData.generateRandomProblems(10)
        self.initialData.generateRandomSolutions(10)
        self.initialData.statuses = list(Status.objects.all())

    def setTestStatuses(self):
        self.awaiting = Status.objects.create(
            name="Scheduled visit", description="Scheduled visit"
        )
        self.completed = Status.objects.create(
            name="Waiting for approval", description="Waiting for approval"
        )
        self.completed = Status.objects.create(
            name="Scheduled service", description="Scheduled service"
        )
        self.completed = Status.objects.create(
            name="Awaiting payment", description="Awaiting payment"
        )
        self.completed = Status.objects.create(
            name="Concluded", description="Concluded", is_conclusive=True
        )
        self.completed = Status.objects.create(name="Canceled", description="Canceled")

    def test_initial_brands_count_is_the_same(self):
        brandCount = Brand.objects.count()
        self.assertEqual(len(self.initialData.brands), brandCount)

    def test_initial_status_count_is_the_same(self):
        statusCount = Status.objects.count()
        self.assertEqual(len(self.initialData.statuses), statusCount)

    def test_initial_categories_count_is_the_same(self):
        categoryCount = Category.objects.count()
        self.assertEqual(len(self.initialData.categories), categoryCount)

    def test_initial_organization_count_is_the_same(self):
        organizationCount = Organization.objects.count()
        self.assertEqual(organizationCount, 1)

    def test_initial_appliances_count_is_the_same(self):
        appliancesCount = Appliance.objects.count()
        self.assertEqual(len(self.initialData.appliances), appliancesCount)

    def test_initial_symptoms_count_is_the_same(self):
        symptomsCount = Symptom.objects.count()
        self.assertEqual(len(self.initialData.symptoms), symptomsCount)
