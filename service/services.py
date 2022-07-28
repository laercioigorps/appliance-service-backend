from appliances.models import Appliance, Brand, Problem, Solution, Symptom
from appliances.tests.factories import (
    ApplianceFactory,
    BrandFactory,
    CategoryFactory,
    ProblemFactory,
    SolutionFactory,
    SymptomFactory,
)
from service.models import Status
from core.utils.tests.base import faker


class SampleDataCreation:
    def __init__(self):
        self.customers = []
        self.statuses = []
        self.organization = None
        self.appliances = []
        self.symptoms = []
        self.problems = []
        self.solutions = []
        self.services = []

    def fetchInitialData(self):
        self.statuses = list(Status.objects.all())
        self.appliances = list(Appliance.objects.all())
        self.symptoms = list(Symptom.objects.all())
        self.problems = list(Problem.objects.all())
        self.solutions = list(Solution.objects.all())


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

    def generateRandonStatus(self, quantity):
        for i in range(quantity):
            self.statuses.append(
                Status.objects.create(name=faker.color_name(), description="status")
            )

    def setRandomStatusAsConclusive(self, quantity):
        randomStatus = faker.random_element(self.statuses)
        randomStatus.is_conclusive = True
        randomStatus.save()

    def generateRandomSymptoms(self, quantity):
        self.symptoms = SymptomFactory.create_batch(quantity)

    def generateRandomProblems(self, quantity):
        self.problems = ProblemFactory.create_batch(quantity)

    def generateRandomSolutions(self, quantity):
        self.solutions = SolutionFactory.create_batch(quantity)
