from appliances.models import Brand
from appliances.tests.factories import ApplianceFactory, BrandFactory, CategoryFactory
from service.models import Status
from core.utils.tests.base import faker


class SampleDataCreation:
    def __init__(self):
        self.customers = []
        self.statuses = []
        self.organization = None
        self.appliances = []

    def updateStatuses(self):
        self.statuses = Status.objects.all()


class InitialSampleDataCreation:
    def __init__(self):
        self.brands = []
        self.categories = []
        self.appliances = []
        self.symptoms = []
        self.problems = []
        self.solutions = []
        self.statuses = []

    def generateRandomBrands(self, quantity):
        self.brands = BrandFactory.create_batch(quantity)

    def generateRandomCategories(self, quantity):
        self.categories = CategoryFactory.create_batch(quantity)

    def generateRandomAppliances(self, quantity):
        for i in range(quantity):
            self.appliances.append(
                ApplianceFactory(
                    brand=faker.random_element(elements=self.brands),
                    category=faker.random_element(elements=self.categories),
                )
            )
