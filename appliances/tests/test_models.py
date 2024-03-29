from unicodedata import category
from django.test import TestCase
from appliances.models import (
    Brand,
    Category,
    Appliance,
    Symptom,
    Problem,
    Solution,
    Historic,
)
from profiles.models import Organization
from .factories import (
    ApplianceFactory,
    BrandFactory,
    CategoryFactory,
    HistoricFactory,
    ProblemFactory,
    SolutionFactory,
    SymptomFactory,
)

# Create your tests here.


class BrandTest(TestCase):
    def test_create_brand(self):
        brandCount = Brand.objects.all().count()

        Brand.objects.create(name="Brastemp")
        myBrand = Brand.objects.get(name="Brastemp")
        self.assertEquals(myBrand.name, "Brastemp")

        newBrandCount = Brand.objects.all().count()
        self.assertEqual(newBrandCount, brandCount + 1)

    def test_create_brand_with_factory(self):
        brandCount = Brand.objects.all().count()

        brand = BrandFactory()

        newBrandCount = Brand.objects.all().count()
        self.assertEqual(newBrandCount, brandCount + 1)


class CategoryTest(TestCase):
    def test_create_category(self):
        catCount = Category.objects.all().count()

        Category.objects.create(name="Geladeira")
        category = Category.objects.get(name="Geladeira")
        self.assertEquals(category.name, "Geladeira")

        newCatCount = Category.objects.all().count()
        self.assertEqual(newCatCount, catCount + 1)

    def test_create_category_using_factory(self):
        catCount = Category.objects.all().count()

        category = CategoryFactory()
        newCatCount = Category.objects.all().count()
        self.assertEqual(newCatCount, catCount + 1)


class ApplianceTest(TestCase):
    def setUp(self):
        self.brand1 = BrandFactory()
        self.category1 = CategoryFactory()

    def test_create_Apliance(self):
        applianceCount = Appliance.objects.all().count()

        Appliance.objects.create(
            model="BWC11ABANA", brand=self.brand1, category=self.category1
        )

        newApplianceCount = Appliance.objects.all().count()
        self.assertEqual(newApplianceCount, applianceCount + 1)

        appliance = Appliance.objects.get(model="BWC11ABANA")

        self.assertEquals(appliance.brand.name, self.brand1.name)
        self.assertEquals(appliance.category.name, self.category1.name)

    def test_create_apliance_using_factory(self):
        applianceCount = Appliance.objects.all().count()

        appliance = ApplianceFactory()

        newApplianceCount = Appliance.objects.all().count()
        self.assertEqual(newApplianceCount, applianceCount + 1)


class SymptomTest(TestCase):
    def test_create_symptom(self):
        symptoms_count = Symptom.objects.all().count()
        self.assertEquals(symptoms_count, 0)

        symptom = Symptom.objects.create(
            name="Não gela o refrigerador",
            description="A parte de baixo da geladeira está refrigerando abaixo do normal",
        )

        symptoms_count = Symptom.objects.all().count()
        self.assertEquals(symptoms_count, 1)

        self.assertEquals(symptom.name, "Não gela o refrigerador")

    def test_create_symptom_using_factory(self):
        symptoms_count = Symptom.objects.all().count()

        symptom = SymptomFactory()

        newSymptoms_count = Symptom.objects.all().count()
        self.assertEquals(newSymptoms_count, symptoms_count + 1)

    def test_add_category_to_symptom(self):
        symptom = Symptom.objects.create(
            name="Não gela o refrigerador", description="A sample description"
        )
        symptoms_count = symptom.categories.all().count()
        self.assertEquals(symptoms_count, 0)

        geladeira = Category.objects.create(name="Geladeira")
        symptom.categories.add(geladeira)

        symptoms_count = symptom.categories.all().count()
        self.assertEquals(symptoms_count, 1)

    def test_add_category_to_symptom_using_factory(self):
        symptom = SymptomFactory(categories=(CategoryFactory(), CategoryFactory()))

        symptoms_count = symptom.categories.all().count()
        self.assertEquals(symptoms_count, 2)

    def test_list_symptoms_by_category(self):
        symptom = Symptom.objects.create(
            name="Não gela o refrigerador", description="A sample description"
        )

        geladeira = Category.objects.create(name="Geladeira")
        symptoms_by_geladeira_count = geladeira.symptom_set.all().count()
        self.assertEquals(symptoms_by_geladeira_count, 0)

        symptom.categories.add(geladeira)

        symptoms_by_geladeira_count = geladeira.symptom_set.all().count()
        self.assertEquals(symptoms_by_geladeira_count, 1)

    def test_add_cause_to_symptom(self):
        bloqueio = Problem.objects.create(name="Evaporador bloqueado")

        symptom = Symptom.objects.create(
            name="Não gela o refrigerador", description="A sample description"
        )
        causes_count = symptom.causes.all().count()
        self.assertEquals(causes_count, 0)

        symptom.causes.add(bloqueio)

        causes_count = symptom.causes.all().count()
        self.assertEquals(causes_count, 1)

    def test_add_cause_to_symptom_using_factory(self):

        symptom = SymptomFactory(causes=(ProblemFactory(), ProblemFactory()))
        causes_count = symptom.causes.all().count()
        self.assertEquals(causes_count, 2)

    def test_symptom__str__(self):
        symptom = Symptom.objects.create(
            name="Não gela o refrigerador", description="A sample description"
        )
        self.assertEqual(str(symptom), "Não gela o refrigerador")


class ProblemTest(TestCase):
    def setUp(self):
        self.solution1 = SolutionFactory()

    def test_create_problem(self):
        problem_count = Problem.objects.all().count()
        self.assertEquals(problem_count, 0)

        problem = Problem.objects.create(
            name="Evaporador bloqueado", description="caso seja frost free"
        )

        problem_count = Problem.objects.all().count()
        self.assertEquals(problem_count, 1)

    def test_add_solution_to_problem(self):

        problem = Problem.objects.create(
            name="Evaporador bloqueado", description="caso seja frost free"
        )
        solution_for_problem_count = problem.solutions.all().count()
        self.assertEquals(solution_for_problem_count, 0)

        problem.solutions.add(self.solution1)

        solution_for_problem_count = problem.solutions.all().count()
        self.assertEquals(solution_for_problem_count, 1)

    def test_problem__str__(self):
        problem = Problem.objects.create(
            name="Evaporador bloqueado", description="caso seja frost free"
        )
        self.assertEqual(str(problem), "Evaporador bloqueado")

    def test_create_problem_using_factory(self):
        problem_count = Problem.objects.all().count()
        self.assertEquals(problem_count, 0)

        problem = ProblemFactory()

        problem_count = Problem.objects.all().count()
        self.assertEquals(problem_count, 1)

    def test_add_solution_to_problem_using_factory(self):

        problem = ProblemFactory(
            solutions=(SolutionFactory(), SolutionFactory(), SolutionFactory())
        )

        solution_for_problem_count = problem.solutions.all().count()
        self.assertEquals(solution_for_problem_count, 3)


class SolutionTest(TestCase):
    def test_create_solution(self):
        solution_count = Solution.objects.all().count()
        self.assertEquals(solution_count, 0)

        solution = Solution.objects.create(
            name="Troca do sensor", description="se for de sensor"
        )

        solution_count = Solution.objects.all().count()
        self.assertEquals(solution_count, 1)

    def test_Solution_str__(self):
        solution = Solution.objects.create(
            name="Troca do sensor", description="se for de sensor"
        )
        self.assertEqual(str(solution), "Troca do sensor")

    def test_create_solution_using_factory(self):
        solution_count = Solution.objects.all().count()
        self.assertEquals(solution_count, 0)

        solution = SolutionFactory()

        solution_count = Solution.objects.all().count()
        self.assertEquals(solution_count, 1)


class ApplianceHistoricTest(TestCase):
    def setUp(self):
        # brands
        self.electrolux = Brand.objects.create(name="Electrolux")
        self.brastemp = Brand.objects.create(name="Brastemp")
        # Cateogories
        self.geladeira = Category.objects.create(name="Geladeira")
        self.lavadoraDeRoupas = Category.objects.create(name="Lavadora de roupas")
        # solutions
        self.trocaDeSensor = Solution.objects.create(
            name="Troca do sensor", description="se for de sensor"
        )
        self.trocaDeplacaDepotencia = Solution.objects.create(
            name="Troca da placa de potencia", description="se for de sensor"
        )
        # Problems
        self.evaporadorBloqueado = Problem.objects.create(
            name="Evaporador bloqueado", description="caso seja frost free"
        )
        self.falhaSensor = Problem.objects.create(
            name="Sensor com falha", description="falha no sensot"
        )
        # Symptoms
        self.naoGelaRefrigerador = Symptom.objects.create(
            name="Não gela o refrigerador",
            description="A parte de baixo da geladeira está refrigerando abaixo do normal",
        )
        self.naoLiga = Symptom.objects.create(
            name="Não liga nada",
            description="não apresenta sinal de energia",
        )

        self.org1 = Organization.objects.create(name="test1")
        self.org2 = Organization.objects.create(name="test2")

    def test_historic_create_with_no_data(self):
        historic = Historic.objects.create()
        self.assertEqual(historic.completed, False)

    def test_historic_create_with_no_data_using_factory(self):
        histCount = Historic.objects.all().count()

        historic = HistoricFactory()

        newHistCount = Historic.objects.all().count()
        self.assertEqual(newHistCount, histCount + 1)

        self.assertEqual(historic.completed, False)

    def test_add_symptoms_to_historic(self):
        historic = Historic.objects.create()

        historic_symptoms_count = historic.symptoms.all().count()
        self.assertEqual(historic_symptoms_count, 0)

        historic.symptoms.add(self.naoGelaRefrigerador)

        historic_symptoms_count = historic.symptoms.all().count()
        self.assertEqual(historic_symptoms_count, 1)

        historic.symptoms.add(self.naoLiga)

        historic_symptoms_count = historic.symptoms.all().count()
        self.assertEqual(historic_symptoms_count, 2)

    def test_add_symptoms_to_historic_using_factory(self):
        historic = HistoricFactory(symptoms=(SymptomFactory(), SymptomFactory()))

        historic_symptoms_count = historic.symptoms.all().count()
        self.assertEqual(historic_symptoms_count, 2)

    def test_add_problems_to_historic(self):
        historic = Historic.objects.create()

        historic_problems_count = historic.problems.all().count()
        self.assertEqual(historic_problems_count, 0)

        historic.problems.add(self.evaporadorBloqueado)

        historic_problems_count = historic.problems.all().count()
        self.assertEqual(historic_problems_count, 1)

        historic.problems.add(self.falhaSensor)

        historic_problems_count = historic.problems.all().count()
        self.assertEqual(historic_problems_count, 2)

    def test_add_problems_to_historic_using_factory(self):
        historic = HistoricFactory(problems=(ProblemFactory(), ProblemFactory()))

        historic_problems_count = historic.problems.all().count()
        self.assertEqual(historic_problems_count, 2)

    def test_add_solution_to_historic(self):
        historic = Historic.objects.create()

        historic_solutions_count = historic.solutions.all().count()
        self.assertEqual(historic_solutions_count, 0)

        historic.solutions.add(self.trocaDeSensor)

        historic_solutions_count = historic.solutions.all().count()
        self.assertEqual(historic_solutions_count, 1)

        historic.solutions.add(self.trocaDeplacaDepotencia)

        historic_solutions_count = historic.solutions.all().count()
        self.assertEqual(historic_solutions_count, 2)

    def test_add_solution_to_historic_using_factory(self):
        historic = HistoricFactory(solutions=(SolutionFactory(), SolutionFactory()))

        historic_solutions_count = historic.solutions.all().count()
        self.assertEqual(historic_solutions_count, 2)

    def test_add_appliance_to_historic(self):
        historic = Historic.objects.create()

        df50x = Appliance.objects.create(
            brand=self.electrolux, category=self.geladeira, model="DF50x"
        )

        self.assertEqual(historic.appliance, None)
        historic.appliance = df50x
        historic.save()

        historicCopy = Historic.objects.get(appliance__model="DF50x")
        self.assertEqual(historicCopy.appliance.model, "DF50x")
        self.assertEqual(historicCopy.appliance.brand.name, "Electrolux")

    def test_add_appliance_to_historic_using_factory(self):
        appliancesCount = Appliance.objects.all().count()
        historic = HistoricFactory()
        NewAppliancesCount = Appliance.objects.all().count()
        self.assertEqual(NewAppliancesCount, appliancesCount + 1)

    def test_add_organization_to_historic(self):
        historic = Historic.objects.create()

        historic.org = self.org1
        historic.save()

        histCopy = Historic.objects.get(pk=historic.id)
        self.assertEquals(histCopy.org.name, self.org1.name)

    def test_add_organization_to_historic_using_factory(self):
        orgCount = Organization.objects.all().count()
        historic = HistoricFactory()
        newOrgCount = Organization.objects.all().count()
        self.assertEqual(newOrgCount, orgCount + 1)
