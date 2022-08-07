from datetime import date
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
        self.start_date = date.today()
        self.end_date = date.today()

    def fetchInitialData(self):
        self.statuses = list(Status.objects.all())
        self.appliances = list(Appliance.objects.all())
        self.symptoms = list(Symptom.objects.all())
        self.problems = list(Problem.objects.all())
        self.solutions = list(Solution.objects.all())

    def generateRandomCustomers(self, quantity):
        for i in range(quantity):
            self.customers.append(
                CustomerFactory(
                    owner=self.organization,
                    created_at=faker.date_between(self.start_date, self.end_date),
                )
            )

    def generateRandomAddressForCustomers(self, quantity):
        for customer in self.customers:
            for i in range(quantity):
                customer.addresses.add(AddressFactory())

    def createRandomHistoric(self):
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
            appliance=None,
            org=None,
        )
        return historic

    def createRandomService(self, customer, historic):
        randomDate = faker.date_between(self.start_date, self.end_date)

        service = ServiceFactory(
            owner=self.organization,
            customer=customer,
            historic=historic,
            address=faker.random_element(customer.addresses.all()),
            status=faker.random_element(self.statuses),
            start_date=randomDate,
        )
        return service

    def generateRandomServices(self, quantity):
        for i in range(quantity):
            customer = faker.random_element(self.customers)
            historic = self.createRandomHistoric()
            service = self.createRandomService(customer, historic)
            if service.status.is_conclusive:
                service.end_date = service.start_date
                service.save()
            self.services.append(service)


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
