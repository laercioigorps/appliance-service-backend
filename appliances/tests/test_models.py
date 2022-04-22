from django.test import TestCase
from appliances.models import Brand, Category, Appliance, Symptom

# Create your tests here.


class BrandTest(TestCase):
    def test_create_brand(self):
        Brand.objects.create(name="Brastemp")
        myBrand = Brand.objects.get(name="Brastemp")
        self.assertEquals(myBrand.name, "Brastemp")


class CategoryTest(TestCase):
    def test_create_category(self):
        Category.objects.create(name="Geladeira")
        category = Category.objects.get(name="Geladeira")
        self.assertEquals(category.name, "Geladeira")


class ApplianceTest(TestCase):

    def setUp(self):
        self.brand1 = Brand.objects.create(name="Brastemp")
        self.category1 = Category.objects.create(name="Geladeira")

    def test_create_Apliance(self):
        Appliance.objects.create(
            model="BWC11ABANA", brand=self.brand1, category=self.category1)
        appliance = Appliance.objects.get(model="BWC11ABANA")
        self.assertEquals(appliance.model, "BWC11ABANA")
        self.assertEquals(appliance.brand.name, "Brastemp")
        self.assertEquals(appliance.category.name, "Geladeira")


class SymptomTest(TestCase):

    def test_create_symptom(self):
        symptoms_count = Symptom.objects.all().count()
        self.assertEquals(symptoms_count, 0)

        symptom = Symptom.objects.create(name="Não gela o refrigerador",
                                         description="A parte de baixo da geladeira está refrigerando abaixo do normal")

        symptoms_count = Symptom.objects.all().count()
        self.assertEquals(symptoms_count, 1)

        self.assertEquals(symptom.name, "Não gela o refrigerador")

    def test_add_category_to_symptom(self):
        symptom = Symptom.objects.create(name="Não gela o refrigerador",
                                         description="A sample description")
        symptoms_count = symptom.categories.all().count()
        self.assertEquals(symptoms_count, 0)

        geladeira = Category.objects.create(name="Geladeira")
        symptom.categories.add(geladeira)

        symptoms_count = symptom.categories.all().count()
        self.assertEquals(symptoms_count, 1)

    def test_list_symptoms_by_category(self):
        symptom = Symptom.objects.create(name="Não gela o refrigerador",
                                         description="A sample description")

        geladeira = Category.objects.create(name="Geladeira")
        symptoms_by_geladeira_count = geladeira.symptom_set.all().count()
        self.assertEquals(symptoms_by_geladeira_count, 0)

        symptom.categories.add(geladeira)

        symptoms_by_geladeira_count = geladeira.symptom_set.all().count()
        self.assertEquals(symptoms_by_geladeira_count, 1)
