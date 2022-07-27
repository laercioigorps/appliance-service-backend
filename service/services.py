from appliances.models import Brand
from appliances.tests.factories import BrandFactory, CategoryFactory
from service.models import Status


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

    def generateRandomBrands(self, quantity):
        self.brands = BrandFactory.create_batch(quantity)

    def generateRandomCategories(self, quantity):
        self.categories = CategoryFactory.create_batch(quantity)
