from appliances.models import Appliance, Brand, Problem, Solution, Symptom
from appliances.tests.factories import (
    ApplianceFactory,
    BrandFactory,
    CategoryFactory,
    HistoricFactory,
    ProblemFactory,
    SolutionFactory,
    SymptomFactory,
)
from profiles.tests.factories import AddressFactory, CustomerFactory
from service.models import Status
from core.utils.tests.base import faker
from service.tests.factories import ServiceFactory


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

    def generateRandomCustomers(self, quantity):
        for i in range(quantity):
            self.customers.append(CustomerFactory(owner=self.organization))

    def generateRandomAddressForCustomers(self, quantity):
        for customer in self.customers:
            for i in range(quantity):
                customer.addresses.add(AddressFactory())

    def generateRandomServices(self, quantity):
        for i in range(quantity):
            historic = HistoricFactory(
                symptoms=faker.random_elements(
                    elements=self.symptoms, unique=True, length=2
                ),
                problems=faker.random_elements(
                    elements=self.problems, unique=True, length=2
                ),
                solutions=faker.random_elements(
                    elements=self.solutions, unique=True, length=2
                ),
            )
            self.services.append(
                ServiceFactory(
                    owner=self.organization,
                    customer=faker.random_element(self.customers),
                    historic=historic,
                )
            )


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
