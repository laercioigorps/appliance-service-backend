from django.test import TestCase
from appliances.models import Appliance, Brand
from appliances.tests.factories import BrandFactory, CategoryFactory
from service.models import Status
from profiles.models import Organization

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
        self.brands = []
        self.sampleData = SampleDataCreation()
        self.organization = Organization.objects.create(name="own")
        self.setTestStatuses()
        self.initialData = InitialSampleDataCreation()
        self.generateInitialData()

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
        self.assertEqual(self.sampleData.statuses, self.initialData.statuses)
        self.assertEqual(self.sampleData.appliances, self.initialData.appliances)
        self.assertEqual(self.sampleData.symptoms, self.initialData.symptoms)
        self.assertEqual(self.sampleData.problems, self.initialData.problems)
        self.assertEqual(self.sampleData.solutions, self.initialData.solutions)
